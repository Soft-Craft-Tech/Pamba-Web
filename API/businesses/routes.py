from API.models import Business
from flask import Blueprint, jsonify, request
from API import db, bcrypt
from API.utilities.auth import business_login_required, verify_api_key, generate_token, decode_token
from API.utilities.slugify import slugify
from API.utilities.send_mail import business_account_activation_email, send_reset_email
from API.utilities.data_serializer import serialize_business
from datetime import datetime, timedelta

business_blueprint = Blueprint("businesses", __name__, url_prefix="/API/businesses")


@business_blueprint.route("/signup", methods=["POST"])
@verify_api_key
def business_signup():
    """
        Signup for Businesses/Business Owners
        :return: 200, 409
    """
    payload = request.get_json()
    name = payload["name"].strip().title()
    category = payload["category"].title()
    email = payload["email"].strip().lower()
    phone = payload["phone"].strip()
    city = payload["city"].strip().title()
    location = payload["location"].strip().title()
    google_map = payload["mapUrl"].strip()
    hashed_password = bcrypt.generate_password_hash(payload["password"].strip()).decode("utf-8")
    slug = slugify(name)

    # Check if email and phone number already exists
    existing_email = Business.query.filter_by(email=email).first()
    existing_phone = Business.query.filter_by(phone=phone).first()

    if existing_email:
        return jsonify({"message": "Email already exists"}), 409

    if existing_phone:
        return jsonify({"message": "Phone number already exists"}), 409

    business = Business(
        business_name=name,
        category=category,
        slug=slug,
        email=email,
        phone=phone,
        city=city,
        location=location,
        google_map=google_map,
        password=hashed_password
    )
    db.session.add(business)
    db.session.commit()

    # Activation Token
    token_expiry_time = datetime.utcnow() + timedelta(minutes=30)
    token = generate_token(expiry=token_expiry_time, username=business.slug)

    # Send mail
    business_account_activation_email(recipient=business.email, token=token, name=business.business_name)

    return jsonify(
        {
            "message": "Successful! Account activation link set to your email",
            "business": serialize_business(business),
        }
    ), 200


@business_blueprint.route("/activate-account/<string:token>", methods=["POST"])
@verify_api_key
def activate_account(token):
    """
        Activate businesses accounts
        :return: 200
    """
    decoded_data = decode_token(token)

    if not decoded_data:
        return jsonify({"message": "Token Invalid or Expired"}), 400

    business = Business.query.filter_by(slug=decoded_data["username"]).first()
    if not business:
        return jsonify({"message": "Not Found"}), 404
    if business.active:
        return jsonify({"message": "Account already active"}), 400
    business.active = True
    db.session.commit()

    return jsonify({"message": "Success"}), 200


@business_blueprint.route("/login", methods=["POST"])
@verify_api_key
def login():
    """
        Businesses login
        :return: 404, 401, 200
    """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Login Required"}), 401

    business = Business.query.filter_by(email=auth.username.strip().lower()).first()

    if not business:
        return jsonify({"message": "Incorrect Email or Password"}), 404

    if not bcrypt.check_password_hash(business.password, auth.password.strip()):
        return jsonify({"message": "Incorrect Email or Password"}), 401

    token_expiry_time = datetime.utcnow() + timedelta(days=30)
    token = generate_token(expiry=token_expiry_time, username=business.slug)

    return jsonify({"message": "Login Successful", "client": serialize_business(business), "authToken": token}), 200


@business_blueprint.route("/request-password-reset", methods=["POST"])
@verify_api_key
def request_password_reset():
    """
        Request for a password reset link.
        Link sent to business email
        :return: 404, 200
    """
    payload = request.get_json()
    email = payload["email"].strip().lower()

    business = Business.query.filter_by(email=email).first()
    if not business:
        return jsonify({"message": "Email doesn't exist"}), 404

    token_expiry_time = datetime.utcnow() + timedelta(minutes=30)
    token = generate_token(expiry=token_expiry_time, username=business.slug)
    send_reset_email(recipient=business.email, token=token, name=business.business_name)

    return jsonify({"message": "Reset link has been sent to your email"}), 200


@business_blueprint.route("/reset-password/<string:reset_token>", methods=["PUT"])
@verify_api_key
def reset_password(reset_token):
    """
        Reset the business's password
        :param reset_token: Reset token give ti the user upon requesting password reset
        :return: 200, 400
    """
    payload = request.get_json()
    new_password = payload["password"]
    password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    decoded_data = decode_token(reset_token)

    if not decoded_data:
        return jsonify({"message": "Reset Token is Invalid or Expired "}), 400

    username = decoded_data["username"]
    business = Business.query.filter_by(slug=username).first()
    business.password = password_hash
    db.session.commit()

    return jsonify({"message": "Password Reset Successful"}), 200


@business_blueprint.route("/resend-activation-token", methods=["POST"])
@business_login_required
def resend_account_activation_token(business):
    """
        Resend account activation token.
        When the token sent at signup is expired or lost
        :return: 200
    """
    username = business.slug
    name = business.business_name
    email = business.email

    token_expiry_time = datetime.utcnow() + timedelta(minutes=30)
    token = generate_token(expiry=token_expiry_time, username=username)
    business_account_activation_email(token=token, recipient=email, name=name)

    return jsonify({"message": "Account activation token has been sent to your email."}), 200
