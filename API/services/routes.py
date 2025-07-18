import datetime

from flask import jsonify, Blueprint, request
from API.models import ServiceCategories, Service, Business
from API.lib.auth import verify_api_key, business_verification_required,business_login_required
from API.lib.data_serializer import serialize_service, serialize_staff, serialize_business
from API import db

services_blueprint = Blueprint("services", __name__, url_prefix="/API/services")


@services_blueprint.route("/categories", methods=["GET"])
@verify_api_key
def fetch_service_categories():
    """
        Fetch all service categories
        :return: 200
    """
    categories = ServiceCategories.query.order_by(ServiceCategories.category_name).all()
    all_categories = []
    for category in categories:
        all_categories.append({"id": category.id, "category": category.category_name})

    return jsonify({"message": "Success", "categories": all_categories}), 200


@services_blueprint.route("/all", methods=["GET"])
@verify_api_key
def fetch_all_services():
    """
        Fetch all services
        :return: 200
    """
    services = db.session.query(Service, Business) \
        .join(Business, Service.business_id == Business.id) \
        .filter(
            Business.active.is_(True),
            Business.verified.is_(True),
            Business.profile_completed.is_(True)
        ) \
        .order_by(Service.service) \
        .all()
        
    serialized_services = []
    for service, business in services:
        serialized = serialize_service(service)
        serialized_business = serialize_business(business)
        record = {"serviceInfo": serialized, "businessInfo": serialized_business}
        serialized_services.append(record)
    return jsonify({"services": serialized_services}), 200


@services_blueprint.route("/retrieve/<int:service_id>", methods=["GET"])
@verify_api_key
def retrieve_service(service_id):
    """
        Retrieve single service.
        :param : Id of the service to be retrieved
    """
    service: Service = Service.query.get(service_id)

    if not service:
        return jsonify({"message": "Not found"}), 404
    serialized_service: dict = serialize_service(service)
    estimated_time: float = serialized_service.pop("estimated_service_time")
    hours: int = int(estimated_time)
    minutes: int = int((estimated_time - hours) * 60)

    if minutes == 0:
        estimated_time_string = f"{hours} Hour(s)"
    else:
        estimated_time_string = f"{hours} Hour(s), {minutes} minutes" if hours != 0 else f"{minutes} minutes"

    business: Business = service.business
    serialized_service["estimated_time_string"] = estimated_time_string
    serialized_service["business_name"] = business.business_name
    serialized_service["weekdayOpening"] = business.weekday_opening.strftime("%H:%M") if business.weekday_opening else None
    serialized_service["weekdayClosing"] = business.weekday_closing.strftime("%H:%M") if business.weekday_closing else None
    serialized_service["weekendOpening"] = business.weekend_opening.strftime("%H:%M") if business.weekend_opening else None
    serialized_service["weekendClosing"] = business.weekend_closing.strftime("%H:%M") if business.weekend_closing else None
    serialized_service["slug"] = business.slug
    serialized_service["phone"] = business.phone
    serialized_service["formatted_address"] = business.formatted_address
    serialized_service["latitude"] = business.latitude
    serialized_service["longitude"] = business.longitude
    serialized_service["place_id"] = business.place_id
    if business.latitude and business.longitude and business.place_id:
        serialized_service["directions"] = f"https://www.google.com/maps/search/?api=1&query={business.latitude},{business.longitude}&query_place_id={business.place_id}"
    else:
        serialized_service["directions"] = None


    staff: list = service.business.staff.all()
    # serialized_staff: list = [serialize_staff(staff) for staff in all_staff]

    return jsonify({"service": serialized_service, "staff": serialize_staff(staff)}), 200


@services_blueprint.route("/update/<int:service_id>", methods=["PUT"])
@business_login_required
@business_verification_required
def update_service(business: Business, service_id: int):
    """
        Update the service
        :param business: Service Owner
        :param service_id: Service ID
        :return: 400, 404, 200
    """
    payload: dict = request.get_json()
    service_name: str = payload.get("name", "").title().strip()
    price: float = payload.get("price", "")
    description: str = payload.get("description", "").strip()
    estimated_service_time: float = payload.get("estimatedTime", "")
    service_category: int = payload.get("category", "")

    service: Service = Service.query.get(service_id)

    if not service:
        return jsonify({"message": "Service doesn't exist"}), 404

    if service.business_id != business.id:
        return jsonify({"message": "Not allowed"}), 400

    service.service = service_name if service_name != "" else service.service
    service.price = price if price != "" else service.price
    service.description = description if description != "" else service.description
    service.estimated_service_time = estimated_service_time if estimated_service_time != "" else service.estimated_service_time
    service.service_category = service_category if service_category != "" else service.service_category

    db.session.commit()

    return jsonify({"message": "Service Update successfully", "service": serialize_service(service)}), 200


@services_blueprint.route("/delete/<int:service_id>", methods=["DELETE"])
@business_login_required
@business_verification_required
def delete_service(business: Business, service_id: int):
    """
        Delete Service
        :param business: Owner Id
        :param service_id: Service to be deleted
        :return: 400, 404, 200
    """
    service: Service = Service.query.get(service_id)

    if not service:
        return jsonify({"message": "Service doesn't exist"}), 404

    if service.business_id != business.id:
        return jsonify({"message": "Not allowed"}), 400

    db.session.delete(service)
    db.session.commit()

    return jsonify({"message": "Service Deleted successfully"}), 200

