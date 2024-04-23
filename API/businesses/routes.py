from API.models import Business, Appointment, Sale, ServicesBusinessesAssociation, Service, Rating, Review
from flask import Blueprint, jsonify, request
from API import db, bcrypt
from API.lib.auth import business_login_required, verify_api_key, generate_token, decode_token, client_login_required
from API.lib.slugify import slugify
from API.lib.send_mail import business_account_activation_email, send_reset_email
from API.lib.data_serializer import serialize_business, serialize_service, serialize_review, serialize_appointment
from API.lib.rating_calculator import calculate_ratings
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
    phone = payload["phone"]

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
    ), 201


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
    return jsonify({"message": "Success", "username": business.slug}), 200


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

    token_expiry_time = datetime.utcnow() + timedelta(days=1)
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


@business_blueprint.route("/update", methods=["PUT"])
@business_login_required
def update_profile(business):
    """
        Update business profile
        :param business: Logged in business
        :return: 200
    """
    payload = request.get_json()
    name = payload["name"].strip().title()
    email = payload["email"].strip().lower()
    phone = payload["phone"].strip()
    city = payload["city"].strip().title()
    location = payload["location"].strip().title()
    description = payload["description"]
    google_map = payload["mapUrl"].strip()
    password = payload["password"].strip()
    slug = business.slug if business.business_name == name else slugify(name)

    if not bcrypt.check_password_hash(business.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    # Check if email and phone number already exists
    existing_email = Business.query.filter_by(email=email).first()
    existing_phone = Business.query.filter_by(phone=phone).first()

    if existing_email and existing_email.email != business.email:
        return jsonify({"message": "Email already exists"}), 409

    if existing_phone and existing_phone.phone != business.phone:
        return jsonify({"message": "Phone number already exists"}), 409

    business.business_name = name
    business.email = email
    business.phone = phone
    business.city = city
    business.location = location
    business.google_map = google_map
    business.slug = slug
    business.description = description
    db.session.commit()

    return jsonify({"message": "Update Successful"}), 200


@business_blueprint.route("/change-password", methods=["PUT"])
@business_login_required
def change_password(business):
    """
        Allow the business owner to change their password
        :param business: logged in business
        :return: 401, 200
    """
    payload = request.get_json()
    new_password = payload["newPassword"]
    old_password = payload["oldPassword"]
    password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

    if not bcrypt.check_password_hash(business.password, old_password):
        return jsonify({"message": "Old password is incorrect"}), 401

    business.password = password_hash
    db.session.commit()

    return jsonify({"message": "Success! Password has been changed"}), 200


@business_blueprint.route("/assign-services", methods=["POST"])
@business_login_required
def assign_services(business):
    """
        Assign services being offered by business logged in.
        :param business: Logged in business or owner.
        :return: 200
    """
    payload = request.get_json()
    services = payload["services"]

    if len(services) == 0:
        return jsonify({"message": "No service to be added"}), 400

    service_ids = {service["id"]: service["price"] for service in services}
    services_to_associate = Service.query.filter(Service.id.in_(service_ids.keys())).all()

    # Find services already offered by the business so that a service is not listed twice for the same business
    this_business_services = ServicesBusinessesAssociation.query.filter_by(business_id=business.id).all()
    this_business_services_ids = [item.service_id for item in this_business_services]
    try:
        for service in services_to_associate:
            if service.id in this_business_services_ids:
                continue
            business_service_association = ServicesBusinessesAssociation(
                business_id=business.id,
                service_id=service.id,
                price=service_ids[service.id]
            )
            db.session.add(business_service_association)
            db.session.commit()
    except:
        return jsonify({"message": "An error occurred please try again"}), 500

    return jsonify({"message": "Services have been Added"}), 200


@business_blueprint.route("/remove-service", methods=["POST"])
@business_login_required
def remove_service(business):
    """
        Remove a services from the business
        :param business: Logged  in business
        :return: 404, 200
    """
    payload = request.get_json()
    service_id = payload["serviceId"]

    service = ServicesBusinessesAssociation.query.filter_by(service_id=service_id, business_id=business.id).first()

    if not service:
        return jsonify({"message": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()

    return jsonify({"message": "Service removed"}), 200


@business_blueprint.route("/all-businesses", methods=["GET"])
@verify_api_key
def fetch_all_businesses():
    """
        Fetch all businesses
        :return: 200
    """
    businesses = Business.query.filter_by(active=True).all()
    all_businesses = []
    for business in businesses:
        business_data = serialize_business(business)
        all_businesses.append(business_data)
    return jsonify({"message": "Success", "businesses": all_businesses}), 200


@business_blueprint.route("/<string:slug>", methods=["GET"])
@client_login_required
def fetch_business(client, slug):
    """
        Fetch business by a give ID
        :param client:
        :param slug:
        :return: 404, 200
    """

    business = Business.query.filter_by(slug=slug).first()

    if not business:
        return jsonify({"message": "Business doesn't exist"}), 404

    if not business.active:
        return jsonify({"message": "Business not verified"}), 400

    ratings = Rating.query.filter_by(business_id=business.id).all()
    if ratings:
        rating_score, breakdown = calculate_ratings(ratings=ratings, breakdown=True)
    else:
        breakdown = None
        rating_score = None
    reviews = Review.query.filter_by(business_id=business.id)
    business_data = dict(
        name=business.business_name,
        category=business.category,
        id=business.id,
        location=business.location,
        phone=business.phone,
        google_map=business.google_map,
        description=business.description,
        imageUrl=business.profile_img,
        city=business.city,
        email=business.email
    )

    all_services = []
    for service in business.services.all():
        service_price = ServicesBusinessesAssociation.query\
            .filter_by(business_id=business.id, service_id=service.id).first()
        service_info = serialize_service(service)
        service_info["price"] = service_price.price
        all_services.append(service_info)

    all_reviews = []
    for review in reviews:
        all_reviews.append(serialize_review(review))

    return jsonify(
        {
            "business": business_data,
            "services": all_services,
            "ratingsAverage": rating_score,
            "ratingsBreakdown": breakdown,
            "reviews": all_reviews,
            "gallery": []
        }
    ), 200


@business_blueprint.route("/analysis", methods=["GET"])
@business_login_required
def get_business_analytics(business):
    """
        Business analysis for the Business Dashboard Page
        :param business: Logged in Business
        :return: 200
    """
    # Today's Appointments
    today = datetime.today().date()
    current_month = today.month
    current_year = today.year
    appointments = Appointment.query.filter_by(date=today, business_id=business.id).all()
    today_appointments = []
    for appointment in appointments:
        appointment_serialized = serialize_appointment(appointment)
        appointment_serialized["service"] = appointment.service.service
        today_appointments.append(appointment_serialized)

    # Today's Revenue & current month Revenue
    sales = Sale.query.filter_by(business_id=business.id).all()
    sales_sum = 0
    current_month_sales = 0
    for sale in sales:
        service = ServicesBusinessesAssociation.query.filter_by(business_id=business.id, service_id=sale.service_id) \
            .first()
        if sale.date_created.date().month == current_month and sale.date_created.date().year == current_year:
            if sale.date_created.date() == today:
                sales_sum += service.price
            current_month_sales += service.price

    return jsonify(
        {
            "message": "yes",
            "today_appointments": today_appointments,
            "today_revenue": sales_sum,
            "current_month_revenue": current_month_sales
        }
    ), 200


@business_blueprint.route("/service-businesses/<int:service_id>", methods=["GET"])
@client_login_required
def service_businesses(client, service_id):
    """
        Get business by service. Businesses offering a certain service
        :param client:
        :param service_id: ID of the service
        :return: 404, 200
    """
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"message": "Service doesn't exist"}), 404

    all_businesses = []
    for business in service.businesses:
        ratings = Rating.query.filter_by(business_id=business.id).all()
        rating_score = calculate_ratings(ratings=ratings, breakdown=False)
        business_info = dict(
            name=business.business_name,
            category=business.category,
            city=business.city,
            google_map=business.google_map,
            id=business.id,
            phone=business.phone,
            location=business.location,
            ratingsAverage=rating_score
        )
        all_businesses.append(business_info)

    return jsonify({"businesses": all_businesses}), 200


@business_blueprint.route("/upload-profile-img", methods=["PUT"])
@business_login_required
def upload_profile_img(business):
    """
        Allow businesses to upload the profile image
        :param business: Business logged-in
        :return: 200
    """
    payload = request.get_json()

    try:
        image_url = payload["imageURL"]
    except KeyError:
        return jsonify({"message": "No Image to be Uploaded"}), 400

    business.profile_img = image_url
    db.session.commit()

    return jsonify({"message": "Success"}), 200


@business_blueprint.route("/update-description", methods=["PUT"])
@business_login_required
def update_description(business):
    """
        Add the Business Description to the Business
        :param business: Logged in Business
        :return: 400, 200
    """
    payload = request.get_json()

    try:
        description = payload["description"]
    except KeyError:
        return jsonify({"message": "No description added"}), 400

    business.description = description
    db.session.commit()

    return jsonify({"message": "Update Successful"}), 200


@business_blueprint.route("/profile-completion-status", methods=["GET"])
@business_login_required
def profile_completion_status(business):
    """
        Check Profile Update States
        :param business: Logged in business
        :return: 200
    """
    payload = {
        "profileImg": False,
        "description": False,
        "services": False,
        "expenseAccounts": False
    }
    services = ServicesBusinessesAssociation.query.filter_by(business_id=business.id).all()
    accounts = business.expense_accounts.all()
    if business.profile_img:
        payload["profileImg"] = True

    if business.description:
        payload["description"] = True

    if len(accounts) != 0:
        payload["expenseAccounts"] = True

    if len(services) != 0:
        payload["services"] = True

    return jsonify(payload), 200

