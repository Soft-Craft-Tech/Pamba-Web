from flask import jsonify, request
from API.models import Client
from API.utilities.data_serializer import serialize_client
from API.utilities.auth import verify_api_key
from flask import Blueprint
from API import bcrypt, db
from API.utilities.OTP import generate_otp
from API.utilities.emails import send_otp
from datetime import datetime, timedelta
import jwt
import os

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
    phone = payload["phone"].strip()

    # Check for existence of user with same email or phone number
    email_exists = Client.query.filter_by(email=email).first()
    if email_exists:
        return jsonify({"message": "Email already exists!"}), 409

    phone_exists = Client.query.filter_by(phone=phone).first()
    if phone_exists:
        return jsonify({"message": "Phone number already exists!"}), 409

    # Hash the password
    password_hash = bcrypt.generate_password_hash(payload["password"].strip()).decode("utf-8")

    otp, otp_hash = generate_otp()
    client = Client(
        name=payload["name"].strip().title(),
        email=email,
        phone=phone,
        password=password_hash,
        otp=otp_hash,
        otp_expiration=datetime.now() + timedelta(minutes=5)
    )
    db.session.add(client)
    db.session.commit()

    # Send Email
    send_otp(recipient=email, otp=otp)

    return jsonify({"message": "Signup Success. An OTP has been sent to your email.", "email": email, "otp": otp}), 200


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
        return jsonify({"message": "Email doesn't exist"}), 404

    if not bcrypt.check_password_hash(client.password, auth.password.strip()):
        return jsonify({"message": "Incorrect Password"}), 401

    token_expiry_time = datetime.utcnow() + timedelta(days=30)
    token_expiry_timestamp = token_expiry_time.timestamp()
    token = jwt.encode(
        {
            "email": client.email,
            "exp": token_expiry_timestamp
        },
        os.environ.get('SECRET'),
        algorithm="HS256"
    )

    return jsonify({"message": "Login Successful", "client": serialize_client(client), "authToken": token}), 200



