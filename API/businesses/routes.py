from API.models import (
    Business, Service, Rating, Review, BusinessCategory,
    ServiceCategories
)
from flask import Blueprint, jsonify, request
from API import db, bcrypt
from API.lib.auth import business_login_required, verify_api_key, generate_token, decode_token
from API.lib.slugify import slugify
from API.lib.send_mail import business_account_activation_email, send_reset_email
from API.lib.data_serializer import (serialize_business,
                                     serialize_service,
                                     serialize_review, serialize_appointment, serialize_business_category,
                                     serialize_sale, serialize_expenses)
from API.lib.rating_calculator import calculate_ratings
from datetime import datetime, timedelta, timezone

business_blueprint = Blueprint("businesses", __name__, url_prefix="/API/businesses")


@business_blueprint.route("/signup", methods=["POST"])
@verify_api_key
def business_signup():
    """
        Signup for Businesses/Business Owners
        :return: 200, 409
    """
    try:
        payload = request.get_json()
        location_obj = payload["location"]
        name = payload["name"].strip().title()
        category = payload["category"]
        email = payload["email"].strip().lower()
        phone = payload["phone"]
        city = payload["city"].strip().title()
        place_id = location_obj.get("place_id")
        formatted_address = location_obj.get("formatted_address", "").strip()
        geometry = location_obj.get("geometry", {}).get("location", {})
        latitude = geometry.get("lat", 0.0)
        longitude = geometry.get("lng", 0.0)
        hashed_password = bcrypt.generate_password_hash(payload["password"].strip()).decode("utf-8")
        slug = slugify(name)

        if not formatted_address or latitude == 0.0 or longitude == 0.0:
            return jsonify({"message": "Invalid location data provided"}), 400

        # Check if email and phone number already exists
        existing_email = Business.query.filter_by(email=email).first()
        existing_phone = Business.query.filter_by(phone=phone).first()
        category_id = None

        if existing_email:
            return jsonify({"message": "Email already exists"}), 409

        if existing_phone:
            return jsonify({"message": "Phone number already exists"}), 409

        try:
            id_ = int(category)  # ID of category
            business_category = BusinessCategory.query.filter_by(id=id_).first()
            if not business_category:
                return jsonify({"message": "Invalid Category"}), 400
            category_id = business_category.id
        except ValueError:
            new_business_category = BusinessCategory(
                category_name=category.strip().title()
            )
            db.session.add(new_business_category)
            db.session.commit()
            category_id = new_business_category.id

        business = Business(
            business_name=name,
            slug=slug,
            email=email,
            phone=phone,
            city=city,
            place_id=place_id,
            formatted_address=formatted_address,
            latitude=latitude,
            longitude=longitude,
            password=hashed_password,
            category_id=category_id
        )
        db.session.add(business)
        db.session.commit()

    # Activation Token
        token_expiry_time = datetime.now(timezone.utc) + timedelta(minutes=30)
        token = generate_token(expiry=token_expiry_time, username=business.slug)

        # Send mail
        business_account_activation_email(recipient=business.email, token=token, name=business.business_name)

        return jsonify(
            {
                "message": "Successful! Account activation link set to your email",
                "business": serialize_business(business),
                "activationToken": token
            }
        ), 201

    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        return jsonify({"message": "Failed to create business due to an unexpected issue"}), 400


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
    try:
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
    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        return jsonify({"message": "Failed to reset password due to an unexpected issue"}), 400


@business_blueprint.route("/resend-activation-token", methods=["POST"])
@business_login_required
def resend_account_activation_token(business):
    """
        Resend account activation token for logged-in, unactivated businesses.
        Expected payload: {} (empty JSON body; no data required)
        :return: 200 on success, 400 if already active or invalid request.
    """
    try:
        if business.active:
            return jsonify({"message": "Account already activated"}), 400

        token_expiry_time = datetime.utcnow() + timedelta(minutes=30)
        token = generate_token(expiry=token_expiry_time, username=business.slug)
        business_account_activation_email(token=token, recipient=business.email, name=business.business_name)

        return jsonify({
            "message": "Account activation token has been sent to your email",
            "activationToken": token
        }), 200
    except Exception:
        return jsonify({"message": "Failed to send activation email due to an unexpected issue"}), 400
    
@business_blueprint.route("/update", methods=["PUT"])
@business_login_required
def update_profile(business):
    """
        Update business profile
        :param business: Logged in business
        :return: 200
    """
    try:
        payload: dict = request.get_json()
        name: str = payload.get("name").strip().title()
        email: str = payload.get("email").strip().lower()
        phone: str = payload.get("phone").strip()
        city: str = payload.get("city").strip().title()
        location: str = payload.get("location").strip().title()
        description: str = payload.get("description")
        google_map: str = payload.get("mapUrl").strip()
        password: str = payload.get("password").strip()
        slug: str = business.slug if business.business_name == name else slugify(name)

        if not bcrypt.check_password_hash(business.password, password):
            return jsonify({"message": "Incorrect password"}), 401

        # Check if email and phone number already exists
        existing_email: Business = Business.query.filter_by(email=email).first()
        existing_phone: Business = Business.query.filter_by(phone=phone).first()

        if existing_email and existing_email.email != business.email:
            return jsonify({"message": "Email already exists"}), 409

        if existing_phone and existing_phone.phone != business.phone:
            return jsonify({"message": "Phone number already exists"}), 409

        token_expiry_time = datetime.utcnow() + timedelta(days=1)
        token = generate_token(expiry=token_expiry_time, username=slug)

        business.business_name = name
        business.email = email
        business.phone = phone
        business.city = city
        business.location = location
        business.google_map = google_map
        business.slug = slug
        business.description = description
        db.session.commit()
        return jsonify({"message": "Update Successful", "business": serialize_business(business), "authToken": token}), 200

    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Failed to update business due to an unexpected issue"}), 400


@business_blueprint.route("/change-password", methods=["PUT"])
@business_login_required
def change_password(business):
    """
        Allow the business owner to change their password
        :param business: logged in business
        :return: 401, 200
    """
    try:
        payload = request.get_json()
        new_password = payload["newPassword"]
        old_password = payload["oldPassword"]
        password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

        if not bcrypt.check_password_hash(business.password, old_password):
            return jsonify({"message": "Old password is incorrect"}), 401

        business.password = password_hash
        db.session.commit()
        return jsonify({"message": "Success! Password has been changed"}), 200
    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        return jsonify({"message": "Failed to change password due to an unexpected issue"}), 400


@business_blueprint.route("/assign-services", methods=["POST"])
@business_login_required
def assign_services(business: Business):
    """
        Assign services being offered by business logged in.
        :param business: Logged in business or owner.
        :return: 200
    """
    try:
        payload: dict = request.get_json()
        services: list = payload["services"]

        if len(services) == 0:
            return jsonify({"message": "No service to be added"}), 400

        for service in services:
            try:
                parsedestimatedtime: float = float(service["estimatedTime"])
            except ValueError:
                return jsonify({"message": "Estimate Time should be a number"}), 400

            service_to_add: Service = Service(
                service=service["name"].title().strip(),
                price=service["price"],
                description=service["description"].strip(),
                estimated_service_time=parsedestimatedtime,
                service_category=service["category"],
                service_image=service["imageURL"],
                business_id=business.id
            )
            db.session.add(service_to_add)
        db.session.commit()
        return jsonify({"message": "Services have been Added"}), 201
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Failed to add services due to an unexpected issue"}), 400


@business_blueprint.route("/remove-service", methods=["POST"])
@business_login_required
def remove_service(business):
    """
        Remove a services from the business
        :param business: Logged  in business
        :return: 404, 200
    """
    try:
        payload = request.get_json()
        service_id = payload["serviceId"]

        service = Service.query.get(service_id)

        if not service:
            return jsonify({"message": "Service not found"}), 404

        db.session.delete(service)
        db.session.commit()
        return jsonify({"message": "Service removed"}), 200
    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        return jsonify({"message": "Failed to remove service due to an unexpected issue"}), 400


@business_blueprint.route("/all-businesses", methods=["GET"])
@verify_api_key
def fetch_all_businesses():
    """
        Fetch all businesses
        :return: 200
    """
    try:
        businesses = Business.query.filter_by(active=True).all()
        all_businesses = []
        for business in businesses:
            business_data = serialize_business(business)
            business_data["reviews"] = len(business.reviews.all())
        all_businesses.append(business_data)
        return jsonify({"message": "Success", "businesses": all_businesses}), 200
    except Exception:
        return jsonify({"message": "Failed to fetch businesses due to an unexpected issue"}), 400


@business_blueprint.route("/<string:slug>", methods=["GET"])
@verify_api_key
def fetch_business(slug):
    """
        Fetch business by a give ID
        :param slug:
        :return: 404, 200
    """
    try:
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
            business_name=business.business_name,
            category=business.category.category_name,
            id=business.id,
            location=business.location,
            phone=business.phone,
            google_map=business.google_map,
            description=business.description,
            imageUrl=business.profile_img,
            city=business.city,
            email=business.email,
            rating=business.rating
        )

        all_services = []
        for service in business.services.all():
            service_info = serialize_service(service)
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
    except Exception:
        return jsonify({"message": "Failed to fetch business due to an unexpected issue"}), 400


@business_blueprint.route("/analysis", methods=["GET"])
@business_login_required
def get_business_analytics(business):
    """
        Business analysis for the Business Dashboard Page
        :param business: Logged in Business
        :return: 200
    """
    # Today's Appointments & all appointments
    try:
        today = datetime.today().date()
        current_month = today.month
        current_year = today.year
        appointments = business.appointments.filter_by(cancelled=False).all()
        today_appointments = []
        all_appointments = []
        for appointment in appointments:
            all_appointments.append(serialize_appointment(appointment))
            if appointment.date == today and not appointment.completed:
                appointment_serialized = serialize_appointment(appointment)
                appointment_serialized["service"] = appointment.service.service
                today_appointments.append(appointment_serialized)

        # Today's Revenue & current month Revenue
        sales = business.sales.all()
        today_sales = 0
        current_month_sales = 0
        lifetime_sales = []
        for sale in sales:
            service = sale.service
            sale_serialized = serialize_sale(sale)
            sale_serialized["price"] = service.price
            lifetime_sales.append(sale_serialized)
            if sale.date_created.date().month == current_month and sale.date_created.date().year == current_year:
                if sale.date_created.date() == today:
                    today_sales += service.price
                current_month_sales += service.price

        # Expenses
        expenses = business.expenses.all()
        current_month_expenses = 0
        lifetime_expenses = []
        for expense in expenses:
            lifetime_expenses.append(serialize_expenses(expense))
            if expense.created_at.date().month == current_month and expense.created_at.date().year == current_year:
                current_month_expenses += expense.amount

        return jsonify(
            {
                "message": "Success",
                "all_appointments": all_appointments,
                "today_appointments": today_appointments,
                "today_revenue": today_sales,
                "current_month_revenue": current_month_sales,
                "lifetime_sales": lifetime_sales,
                "current_month_expenses": current_month_expenses,
                "lifetime_expenses": lifetime_expenses
            }
        ), 200
    except Exception:
        return jsonify({"message": "Failed to fetch business analytics due to an unexpected issue"}), 400


@business_blueprint.route("/service-businesses/<int:service_id>", methods=["GET"])
@verify_api_key
def service_businesses(service_id):
    """
        Get business by service. Businesses offering a certain service
        :param service_id: ID of the service
        :return: 404, 200
    """
    try:
        service_category = ServiceCategories.query.get(service_id)
        if not service_category:
            return jsonify({"message": "Service doesn't exist"}), 404

        all_businesses = []
        for service in service_category.services.all():
            business = service.business
            ratings = Rating.query.filter_by(business_id=business.id).all()
            rating_score = calculate_ratings(ratings=ratings, breakdown=False)
            business_info = dict(
                name=business.business_name,
                categories=[category.category_name for category in business.category],
                city=business.city,
                google_map=business.google_map,
                id=business.id,
                phone=business.phone,
                location=business.location,
                ratingsAverage=rating_score
            )
            all_businesses.append(business_info)

        return jsonify({"businesses": all_businesses}), 200
    except Exception:
        return jsonify({"message": "Failed to fetch businesses due to an unexpected issue"}), 400


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


@business_blueprint.route("/profile-completion-status/", methods=["GET"])
@business_login_required
def profile_completion_status(business):
    """
        Check Profile Update States
        :param business: Logged in business
        :return: 200
    """
    try:
        payload = {
            "profileImg": False,
            "description": False,
            "services": False,
            "expenseAccounts": False,
            "openingAndClosing": False
        }
        services = Service.query.filter_by(business_id=business.id).all()
        accounts = business.expense_accounts.all()
        if business.profile_img:
            payload["profileImg"] = True

        if business.description:
            payload["description"] = True

        if len(accounts) != 0:
            payload["expenseAccounts"] = True

        if len(services) != 0:
            payload["services"] = True

        if business.weekday_opening and business.weekday_closing and business.weekend_opening and business.weekend_closing:
            payload["openingAndClosing"] = True

        return jsonify(payload), 200
    except Exception:
        return jsonify({"message": "Failed to fetch profile completion status due to an unexpected issue"}), 400


@business_blueprint.route("/fetch-business-categories", methods=["GET"])
@verify_api_key
def fetch_business_categories():
    """
        Fetch Business Categories
        :return: 200
    """
    try:
        all_categories = []
        categories = BusinessCategory.query.order_by(BusinessCategory.category_name).all()
        for category in categories:
            all_categories.append(serialize_business_category(category))

        return jsonify({"message": "Successful", "categories": all_categories}), 200
    except Exception:
        return jsonify({"message": "Failed to fetch business categories due to an unexpected issue"}), 400


@business_blueprint.route("/business-hours", methods=["PUT"])
@business_login_required
def add_business_hours(business):
    """
        Add the business Operating hours
        :param business: Logged in business
        :return: 200
    """
    try:
        payload = request.get_json()
        weekday_opening = datetime.strptime(payload["weekdayOpening"], '%H:%M').time()
        weekday_closing = datetime.strptime(payload["weekdayClosing"], '%H:%M').time()
        weekend_opening = datetime.strptime(payload["weekendOpening"], '%H:%M').time()
        weekend_closing = datetime.strptime(payload["weekendClosing"], '%H:%M').time()
   

        business.weekday_opening = weekday_opening
        business.weekday_closing = weekday_closing
        business.weekend_opening = weekend_opening
        business.weekend_closing = weekend_closing

        db.session.commit()
        return jsonify({"message": "Successful! Business hours added"}), 200
    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except ValueError:
        return jsonify({"message": "Invalid Time format. Time format MUST be (12:00)"}), 400
    except Exception:
        return jsonify({"message": "Failed to add business hours due to an unexpected issue"}), 400


@business_blueprint.route("/business-services/<string:slug>", methods=["GET"])
@verify_api_key
def fetch_business_services(slug):
    """
        Fetch Services associated with a certain business
        :param slug: Business slug value
        :return: 200
    """
    try:
        business: Business = Business.query.filter_by(slug=slug).first()
        if not business:
            return jsonify({"message": "Business doesn't exist"}), 404

        services: list = business.services.all()

        all_services: list = []
        for service in services:
            service_object: dict = serialize_service(service)
            service_object["category_name"] = service.category.category_name
            all_services.append(service_object)

        return jsonify(
            {"message": "Success", "services": all_services}
        ), 200
    except Exception:
        return jsonify({"message": "Failed to fetch business services due to an unexpected issue"}), 400
