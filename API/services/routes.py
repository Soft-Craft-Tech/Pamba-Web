from flask import request, jsonify, Blueprint
from API.models import ServiceCategories
from API.lib.auth import verify_api_key
from API.lib.data_serializer import serialize_service

services_blueprint = Blueprint("services", __name__, url_prefix="/API/services")


@services_blueprint.route("/fetch_all", methods=["GET"])
@verify_api_key
def fetch_all_services():
    """
        Fetch all services listed
        :return: 200
    """
    categories = ServiceCategories.query.all()
    all_categories = []
    for category in categories:
        all_categories.append({"id": category.id, "category": category.category_name})

    return jsonify({"message": "Success", "categories": all_categories}), 200
