from flask import jsonify, request, Blueprint
from sqlalchemy import func

from API.models import Client, ClientDeleted, Appointment, Gender
from API.lib.data_serializer import serialize_client, serialize_appointment
from API.lib.utils import save_response_image
from API.lib.auth import verify_api_key, generate_token, decode_token, client_login_required, business_login_required
from API import bcrypt, db
from API.lib.OTP import generate_otp
from API.lib.send_mail import send_otp, sent_client_reset_token
from datetime import datetime, timedelta, date, UTC, timezone
import json

clients_blueprint = Blueprint("clients", __name__, url_prefix="/API/clients")


@clients_blueprint.route("/signup", methods=["POST"])
@verify_api_key
def client_signup():
    """
        Signup new client
        :return: 200, 409
    """
    try:
        payload = request.get_json()
        email = payload["email"].strip().lower()
        phone = payload["phone"]
        name = payload["name"].strip().title()
        otp, otp_hash = generate_otp()
        password_hash = bcrypt.generate_password_hash(payload["password"].strip()).decode("utf-8")

        email_exists = Client.query.filter_by(email=email).first()
        phone_exists = Client.query.filter_by(phone=phone).first()

        if email_exists or phone_exists:
            if email_exists and email_exists.name and email_exists.password:
                return jsonify({"message": "Email already exists!"}), 409

            if phone_exists and phone_exists.name and phone_exists.password:
                return jsonify({"message": "Phone number already exists!"}), 409

            client = email_exists or phone_exists
            client.email = email
            client.phone = phone
            client.name = name
            client.password = password_hash
            client.otp = otp_hash
            client.otp_expiration = datetime.now() + timedelta(minutes=30)
            db.session.commit()

            send_otp(recipient=email, otp=otp, name=name)

        client = Client(
            name=name,
            email=email,
            phone=phone,
            password=password_hash,
            otp=otp_hash,
            otp_expiration=datetime.now() + timedelta(minutes=30)
        )
        db.session.add(client)
        db.session.commit()
        otp_sent = send_otp(recipient=email, otp=otp, name=name)
        return jsonify({"message": "Signup Success. An OTP has been sent to your email.", "email": email if otp_sent else "Signup successful. Please try again",
                        "Client": serialize_client(client)
                        }), 200
    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        return jsonify({"message": "Failed to create business due to an unexpected issue"}), 400


@clients_blueprint.route("/verify-otp", methods=["POST"])
@verify_api_key
def verify_client_otp():
    """
        Verify account with OTP after signup
        :return: 404, 200
    """
    payload = request.get_json()
    email = payload["email"]
    client = Client.query.filter_by(email=email).first()
    received_otp = payload["otp"]

    if not client:
        return jsonify({"message": "User not found"}), 404

    if not client.otp and client.verified:
        return jsonify({"message": "Your account is verified"}), 400

    if not received_otp:
        return jsonify({"message": "OTP not provided"}), 400

    if datetime.now() > client.otp_expiration:
        return jsonify({"message": "OTP Expired"}), 400

    if not bcrypt.check_password_hash(client.otp, received_otp):
        return jsonify({"message": "Invalid OTP"}), 400

    client.verified = True
    client.otp = None
    client.otp_expiration = None
    db.session.commit()

    return jsonify({"message": "Account activated", 
                    "client": serialize_client(client)
                    }), 200


@clients_blueprint.route("/delete-account", methods=["POST"])
@verify_api_key
def request_account_deletion():
    """
        Allow app users to request for deletion of their personal data
        :return: 400, 200
    """
    payload = request.get_json()
    email = payload["email"].strip().lower()
    reason = payload["reason"].strip()

    client = Client.query.filter_by(email=email).first()
    if not client:
        return jsonify({"message": "Email doesn't exist"}), 400

    if client.queued_for_deletion:
        queued_for_delete = ClientDeleted.query.filter_by(email=client.email).first()
        request_date = queued_for_delete.request_date
        days = (datetime.now(UTC)   - request_date).days
        remaining_days = 30 - days
        return jsonify(
            {"message": f"Deletion request was sent on {request_date.date()}. {remaining_days} days remaining."}
        ), 400

    delete_request = ClientDeleted(
        email=email,
        phone=client.phone,
        delete_reason=reason
    )
    try:
        db.session.add(delete_request)
        db.session.commit()

        client.queued_for_deletion = True
        db.session.commit()
        return jsonify({"message": "We are sorry to see you leave. Your data will be deleted in 30 days"}), 200
    except Exception:
        return jsonify({"message": "Failed to delete account due to an unexpected issue"}), 400


@clients_blueprint.route("/login", methods=["POST"])
@verify_api_key
def client_login():
    """
        Client login
        :return: 404, 401, 200
    """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Login Required"}), 401

    client = Client.query.filter_by(email=auth.username.strip().lower()).first()

    if not client:
        return jsonify({"message": "Incorrect Email or Password"}), 401

    if not bcrypt.check_password_hash(client.password, auth.password.strip()):
        return jsonify({"message": "Incorrect Email or Password"}), 401

    if client.queued_for_deletion:
        return jsonify({"message": "Can't Log In. You requested account deletion"}), 400

    token_expiry_time = datetime.now(timezone.utc) + timedelta(days=30)
    token = generate_token(expiry=token_expiry_time, username=client.email)

    return jsonify({"message": "Login Successful", "client": serialize_client(client), "authToken": token}), 200


@clients_blueprint.route("/request-password-reset", methods=["POST"])
@verify_api_key
def request_password_reset():
    """
        Handle forgot password logic.
        Generate token for password reset, send to user.
        Token valid: 30min
        :return: 200, 404
    """
    payload: dict = request.get_json()
    email: str = payload["email"].strip().lower()
    client: Client = Client.query.filter_by(email=email).first()
    if not client:
        return jsonify({"message": "Password reset failed"}), 404

    token_expiry_time: datetime = datetime.utcnow() + timedelta(minutes=30)
    token: str = generate_token(expiry=token_expiry_time, username=client.email)
    token_sent = sent_client_reset_token(
        recipient=client.email,
        url=f"https://www.pamba.africa/client-reset/{token}",
        name=client.name
    )

    return jsonify({"message": "Token sent to your email" if token_sent else "Failed to send token to email. Please check your email after a while"}), 200


@clients_blueprint.route("/reset-password/<string:token>", methods=["POST"])
@verify_api_key
def reset_password(token):
    """
        Reset the password given the jwt token sent to the user.
        :param token: JWT token sent upon requesting password reset
        :return: 200, 401
    """
    payload = request.get_json()
    decoded_info = decode_token(token)

    if not decoded_info:
        return jsonify({"message": "Token invalid or expired"}), 400

    client = Client.query.filter_by(email=decoded_info["username"]).first()
    if not client:
        return jsonify({"message": "Not Found"}), 404
    try:
        new_password = payload["password"]
        new_password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        client.password = new_password_hash
        db.session.commit()

        return jsonify({"message": "Reset Successful"}), 200
    except Exception:
        return jsonify({"message": "Error Resetting Password"})


@clients_blueprint.route("/change-password", methods=["POST"])
@client_login_required
def change_password(client):
    """
        Allow clients to change password at will.
        :param client: Client currently logged in
        :return: 200, 401
    """
    payload = request.get_json()
    old_password = payload["oldPassword"]
    new_password = payload["newPassword"]

    if bcrypt.check_password_hash(client.password, old_password):
        try:
            new_password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
            client.password = new_password_hash
            db.session.commit()
            return jsonify({"message": "Password changed"}), 200
        except:
            return jsonify({"messsage": "Failed to change password"}), 400
    else:
        return jsonify({"message": "Old Password Incorrect"}), 400


@clients_blueprint.route("/update-profile", methods=["POST"])
@client_login_required
def update_profile(client):
    """
        Allow clients to update their profile
        :param client: Client currently logged in
        :return: 409, 400, 200
    """
    payload: dict = json.loads(request.form.get("payload"))
    email: str = payload.get("email").strip().lower()
    phone: str = payload.get("phone").strip()
    files = request.files

    if "image" not in files:
        return jsonify({"message": "No image uploaded"}), 400

    try:
        dob: date = datetime.strptime(payload.get("dob"), "%d-%m-%Y")
    except ValueError:
        return jsonify({"message": "Invalid Date Format"}), 400

    email_taken: Client = Client.query.filter_by(email=email).first()
    phone_taken: Client = Client.query.filter_by(phone=phone).first()

    if email_taken and email_taken.id != client.id:
        return jsonify({"message": "Email already exists"}), 409
    if phone_taken and phone_taken.id != client.id:
        return jsonify({"message": "Phone already taken"}), 409

    image_name = save_response_image(files.get("image"))

    client.email = email
    client.phone = phone
    client.dob = dob
    client.profile_image = image_name
    db.session.commit()

    return jsonify({"message": "Update Successful", "client": serialize_client(client)}), 200


@clients_blueprint.route("/resend-otp", methods=["POST"])
@verify_api_key
def resend_verification_otp():
    """
        Resend Verification OTP incase the users did verify their account at signup
        :return: 404
    """
    payload = request.get_json()
    email = payload["email"].strip().lower()
    client = Client.query.filter_by(email=email).first()
    if not client:
        return jsonify({"message": "Client not found"}), 404

    if client.verified:
        return jsonify({"message": "Your account is already verified"}), 400
    try:
        otp, otp_hash = generate_otp()
        client.otp = otp_hash,
        client.otp_expiration = datetime.now() + timedelta(minutes=5)
        db.session.commit()

        # Send Email
        otp_sent = send_otp(recipient=email, otp=otp, name=client.name)
        masked_email = f"{email[:3]}*****{email.split('@')[-1]}"
        return jsonify({"message": f"OTP sent to: {masked_email}" if otp_sent else "Failure sending the OTP. Please try again"}), 200
    except Exception:
        return jsonify({"message":"Failed to send OTP"}), 400


@clients_blueprint.route("/business-clients", methods=["GET"])
@business_login_required
def fetch_business_clients(business):
    """
        Fetch all clients associated with a certain business
        :param business: Logged in business
        :return: 200
    """
    all_appointments: list = []
    year: int = datetime.now().year
    yearly_appointments: dict = {}

    appointments = business.appointments.filter_by(cancelled=False).order_by(Appointment.date.desc()).all()
    for appointment in appointments:
        all_appointments.append(serialize_appointment(appointment))

        if appointment.date.year == year:
            month = appointment.date.strftime("%b")
            if month in yearly_appointments.keys():
                yearly_appointments[month] += 1
            else:
                yearly_appointments[month] = 1

    client_appointment_counts = db.session.query(Client.id, func.count(Appointment.id)) \
        .join(Appointment) \
        .group_by(Client.id) \
        .having(func.count(Appointment.id) > 1) \
        .all()
    returning_clients = len(client_appointment_counts)

    monthly_appointments: list = [{month: count} for month, count in yearly_appointments.items()]

    business_unique_client = (
        db.session.query(Client)
        .join(Appointment)
        .filter(Appointment.business_id == business.id)
        .distinct()
        .all()
    )

    return jsonify(
        {
            "message": "Success",
            "lifetime_client_number_of_clients": len(business_unique_client),
            "all_clients": serialize_client(business_unique_client),
            "all_appointments": monthly_appointments,
            "returning_clients": returning_clients
        }
    ), 200


@clients_blueprint.route("/retrieve", methods=["GET"])
@client_login_required
def retrieve_client(client: Client):
    """
        Retrieve Client Profile
        :param client: Client Object
        :return: 404, 200
    """

    return jsonify(({"client": serialize_client(client)})), 200

@clients_blueprint.route("/business-clients", methods=["POST"])
@business_login_required
def add_business_clients(business):
    """
    Allow a business to add a new client (name, email, phone, gender).
    Prevent duplicates and associate the client with the business.
    """
    try:
        payload = request.get_json()
        name = payload.get("name", "").strip().title()
        email = payload.get("email", "").strip().lower()
        phone = payload.get("phone", "").strip()
        gender_str = payload.get("gender", "").strip()

        if not all([name, email, phone, gender_str]):
            return jsonify({"message": "All fields (name, email, phone, gender) are required"}), 400

        gender = next((g for g in Gender if g.value.lower() == gender_str.lower()), None)
        if not gender:
            return jsonify({"message": f"Gender must be one of {[g.value for g in Gender]}"}), 400

        if Client.query.filter((Client.email == email) | (Client.phone == phone)).first():
            return jsonify({"message": "Client with this email or phone already exists"}), 409

        new_client = Client(
            name=name,
            email=email,
            phone=phone,
            gender=gender  
        )
        db.session.add(new_client)

        business.clients.append(new_client)
        db.session.commit()
        return jsonify({"message": "Client added successfully", "client": serialize_client(new_client)}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to add client", "error": str(e)}), 500


@clients_blueprint.route("/business-clients/<int:client_id>", methods=["PUT"])
@business_login_required
def edit_business_clients(business, client_id):
    """
    Allow a business to edit a client's details (name, email, phone, gender).
    """
    try:
        payload = request.get_json()
        client = Client.query.get(client_id)

        if not client or client not in business.clients:
            return jsonify({"message": "Client not found or not associated with your business"}), 404

        name = payload.get("name", client.name).strip().title()
        email = payload.get("email", client.email).strip().lower()
        phone = payload.get("phone", client.phone).strip()
        gender_str = payload.get("gender", client.gender.value if client.gender else "").strip()

        if not all([name, email, phone, gender_str]):
            return jsonify({"message": "All fields (name, email, phone, gender) are required"}), 400

        gender = next((g for g in Gender if g.value.lower() == gender_str.lower()), None)
        if not gender:
            return jsonify({"message": f"Gender must be one of {[g.value for g in Gender]}"}), 400

        email_exists = Client.query.filter(Client.email == email, Client.id != client.id).first()
        phone_exists = Client.query.filter(Client.phone == phone, Client.id != client.id).first()
        if email_exists or phone_exists:
            return jsonify({"message": "Email or phone already in use by another client"}), 409

        client.name = name
        client.email = email
        client.phone = phone
        client.gender = gender

        db.session.commit()
        return jsonify({"message": "Client updated successfully", "client": serialize_client(client)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Failed to update client", "error": str(e)}), 500
