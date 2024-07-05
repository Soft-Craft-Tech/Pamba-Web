from flask import jsonify, Blueprint
from API.models import ServiceCategories, Service, Business
from API.lib.auth import verify_api_key
from API.lib.data_serializer import serialize_service, serialize_staff, serialize_business
from API import db
import time

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
    services = db.session.query(Service, Business).order_by(Service.service)\
        .join(Business, Service.business_id == Business.id).all()
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
    serialized_service["slug"] = business.slug
    serialized_service["location"] = business.location
    serialized_service["phone"] = business.phone
    serialized_service["directions"] = business.google_map

    all_staff: list = service.business.staff.all()
    serialized_staff: list = [serialize_staff(staff) for staff in all_staff]

    return jsonify({"service": serialized_service, "staff": serialized_staff}), 200


