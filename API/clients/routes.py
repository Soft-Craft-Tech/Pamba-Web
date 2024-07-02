from flask import jsonify, request, Blueprint
from sqlalchemy import func

from API.models import Client, ClientDeleted, Appointment
from API.lib.data_serializer import serialize_client, serialize_appointment
from API.lib.auth import verify_api_key, generate_token, decode_token, client_login_required, business_login_required
from API import bcrypt, db
from API.lib.OTP import generate_otp
from API.lib.send_mail import send_otp, sent_client_reset_token
from datetime import datetime, timedelta

clients_blueprint = Blueprint("clients", __name__, url_prefix="/API/clients")


@clients_blueprint.route("/signup", methods=["POST"])
@verify_api_key
def client_signup():
    """
        Signup new client
        :return: 200, 409
    """
    payload = request.get_json()
    email = payload["email"].strip().lower()
    phone = payload["phone"]
    name = payload["name"].strip().title()
    otp, otp_hash = generate_otp()
    # Hash the password
    password_hash = bcrypt.generate_password_hash(payload["password"].strip()).decode("utf-8")

    # Check for existence of user with same email or phone number and are not web users who haven't signup
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

    # Send Email
    send_otp(recipient=email, otp=otp, name=name)

    return jsonify({"message": "Signup Success. An OTP has been sent to your email.", "email": email}), 200


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

    return jsonify({"message": "Account activated", "client": serialize_client(client)}), 200


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
        days = (datetime.utcnow() - request_date).days
        remaining_days = 30 - days
        return jsonify(
            {"message": f"Deletion request was sent on {request_date.date()}. {remaining_days} days remaining."}
        ), 400

    delete_request = ClientDeleted(
        email=email,
        phone=client.phone,
        delete_reason=reason
    )
    db.session.add(delete_request)
    db.session.commit()

    client.queued_for_deletion = True
    db.session.commit()

    return jsonify({"message": "We are sorry to see you leave. Your data will be deleted in 30 days"}), 200


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

    if client.queued_for_deletion:
        return jsonify({"message": "Can't Log In. You requested account deletion"}), 400

    if not client:
        return jsonify({"message": "Incorrect Email or Password"}), 404

    if not bcrypt.check_password_hash(client.password, auth.password.strip()):
        return jsonify({"message": "Incorrect Email or Password"}), 401

    token_expiry_time = datetime.utcnow() + timedelta(days=30)
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
    payload = request.get_json()
    email = payload["email"].strip().lower()
    client = Client.query.filter_by(email=email).first()
    if not client:
        return jsonify({"message": "Password reset failed"}), 404

    token_expiry_time = datetime.utcnow() + timedelta(minutes=30)

    token = generate_token(expiry=token_expiry_time, username=client.email)
    sent_client_reset_token(recipient=client.email, token=token, name=client.name)

    return jsonify({"message": "Token sent to your email"}), 200


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
    new_password = payload["password"]
    new_password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    client.password = new_password_hash
    db.session.commit()

    return jsonify({"message": "Reset Successful"}), 200


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
        new_password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        client.password = new_password_hash
        db.session.commit()
        return jsonify({"message": "Password changed"}), 200
    else:
        return jsonify({"message": "Old Password Incorrect"}), 401


@clients_blueprint.route("/update-profile", methods=["POST"])
@client_login_required
def update_profile(client):
    """
        Allow clients to update their profile
        :param client: Client currently logged in
        :return: 409, 200
    """
    payload = request.get_json()
    email = payload["email"].strip().lower()
    phone = payload["phone"].strip()

    email_taken = Client.query.filter_by(email=email).first()
    phone_taken = Client.query.filter_by(phone=phone).first()

    if email_taken and email_taken.id != client.id:
        return jsonify({"message": "Email already exists"}), 409
    if phone_taken and phone_taken.id != client.id:
        return jsonify({"message": "Phone already taken"}), 409

    client.email = email
    client.phone = phone
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

    otp, otp_hash = generate_otp()
    client.otp = otp_hash,
    client.otp_expiration = datetime.now() + timedelta(minutes=5)
    db.session.commit()

    # Send Email
    send_otp(recipient=email, otp=otp, name=client.name)
    masked_email = f"{email[:3]}*****{email.split('@')[-1]}"
    return jsonify({"message": f"OTP sent to: {masked_email}"}), 200


@clients_blueprint.route("/business-clients", methods=["GET"])
@business_login_required
def fetch_business_clients(business):
    """
        Fetch all clients associated with a certain business
        :param business: Logged in business
        :return: 200
    """
    lifetime_number_of_clients: int = 0
    all_clients: list = []
    all_appointments: list = []
    year: int = 2023
    yearly_appointments: dict = {}

    appointments = business.appointments.filter_by(cancelled=False).order_by(Appointment.date.desc()).all()
    for appointment in appointments:
        all_appointments.append(serialize_appointment(appointment))
        client = appointment.client
        lifetime_number_of_clients += 1
        all_clients.append(serialize_client(client))

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

    return jsonify(
        {
            "message": "Success",
            "lifetime_client_number_of_clients": lifetime_number_of_clients,
            "all_clients": all_clients,
            "all_appointments": monthly_appointments,
            "returning_clients": returning_clients
        }
    ), 200
