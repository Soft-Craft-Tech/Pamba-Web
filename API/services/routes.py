from flask import jsonify, Blueprint
from API.models import ServiceCategories, Service
from API.lib.auth import verify_api_key
from API.lib.data_serializer import serialize_service, serialize_staff

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

    services = Service.query.order_by(Service.service).all()
    serialized_services = []
    for service in services:
        serialized = serialize_service(service)
        serialized["business_name"] = service.business.business_name
        serialized["business_location"] = service.business.location
        serialized["business_slug"] = service.business.slug
        serialized["business_profile_image"] = service.business.profile_img
        serialized["business_rating"] = service.business.rating
        serialized["business_reviews"] = service.business.reviews.count()
        serialized_services.append(serialized)

    return jsonify({"services": serialized_services}), 200


@services_blueprint.route("/retrieve/<int:service_id>", methods=["GET"])
@verify_api_key
def retrieve_service(service_id):
    """
        Retrieve single service.
        :param : Id of the service to be retrieved
    """
    service = Service.query.get(service_id)

    if not service:
        return jsonify({"message": "Not found"}), 404
    serialized_service = serialize_service(service)
    estimated_time = serialized_service.pop("estimated_service_time")
    hours = int(estimated_time)
    minutes = int((estimated_time - hours) * 60)

    if minutes == 0:
        estimated_time_string = f"{hours} Hour(s)"
    else:
        estimated_time_string = f"{hours} Hour(s), {minutes} minutes" if hours != 0 else f"{minutes} minutes"

    serialized_service["estimated_time_string"] = estimated_time_string
    serialized_service["business_name"] = service.business.business_name
    serialized_service["slug"] = service.business.slug

    all_staff = service.business.staff.all()
    serialized_staff = [serialize_staff(staff) for staff in all_staff]

    return jsonify({"service": serialized_service, "staff": serialized_staff}), 200


