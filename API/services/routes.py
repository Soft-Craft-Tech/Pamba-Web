from flask import request, jsonify, Blueprint
from API.models import Service
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
    services = Service.query.all()
    all_services = []
    for service in services:
        all_services.append(serialize_service(service))

    return jsonify({"message": "Success", "services": all_services}), 200
