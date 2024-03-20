from API.models import Sale, Service
from flask import Blueprint, jsonify, request
from API import db
from API.lib.auth import business_login_required
from API.lib.data_serializer import serialize_sale

sales_blueprint = Blueprint("sales", __name__, url_prefix="/API/sales")


@sales_blueprint.route("/add-sale", methods=["POST"])
@business_login_required
def record_sale(business):
    """
        Record new Sales
        :param business: Business making the sale
        :return: 200
    """
    payload = request.get_json()
    payment_method = payload["paymentMethod"].strip()
    description = payload["description"].strip()
    service_id = payload["serviceId"]

    business_services = [service.id for service in business.services.all()]
    if service_id not in business_services:
        return jsonify({"message": "We are not offering this service at the moment"}), 400

    sale = Sale(
        payment_method=payment_method,
        description=description,
        service_id=service_id,
        business_id=business.id
    )

    db.session.add(sale)
    db.session.commit()

    return jsonify({"message": "Sale Added", "newSale": serialize_sale(sale)}), 200
