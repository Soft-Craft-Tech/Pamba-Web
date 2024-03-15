from API.models import Business
from flask import Blueprint, jsonify, request
from API import db, bcrypt
from API.utilities.auth import business_login_required, verify_api_key, generate_token
from API.utilities.slugify import slugify
from API.utilities.send_mail import business_account_activation_email
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
    token = generate_token(token_expiry_time, business.email)

    # Send mail
    business_account_activation_email(recipient=business.email, token=token, name=business.business_name)

    return jsonify(
        {
            "message": "Successful! Account activation link set to you email",
            "business": serialize_business(business),
        }
    ), 200
