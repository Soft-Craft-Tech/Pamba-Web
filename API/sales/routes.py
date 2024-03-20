from API.models import Sale
from flask import Blueprint, jsonify, request
from API import db, bcrypt
from API.lib.auth import business_login_required
from API.lib.data_serializer import serialize_sale

sales_blueprint = Blueprint("sales", __name__, url_prefix="/API/sales")


@sales_blueprint.route("/add-sale", methods=["POST"])
@business_login_required
def record_sale(business):
    """
        Record new Sales
        :param business: Business making the sale
        :return: 200, 400
    """
    payload = request.get_json()
    payment_method = payload["paymentMethod"].strip()
    description = payload["description"].strip()
    service_id = payload["serviceId"]

    if not business.active:
        return jsonify({"message": "You need to activate your account first."}), 400

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


@sales_blueprint.route("/all", methods=["GET"])
@business_login_required
def fetch_all_business_sales(business):
    """
        Fetch all the sales for a given business
        :param business: Business
        :return:
    """

    sales = Sale.query.filter_by(business_id=business.id).all()
    all_sales = []

    for sale in sales:
        sale_info = serialize_sale(sale)
        sale_info["service"] = sale.service.service
        all_sales.append(sale_info)

    return jsonify({"message": "Sales", "sales": all_sales})


@sales_blueprint.route("/delete/<int:sale_id>", methods=["DELETE"])
@business_login_required
def delete_sale(business, sale_id):
    """
        Delete a sale
        :param business:
        :param sale_id:
        :return: 404, 400, 200
    """
    payload = request.get_json()
    password = payload["password"].strip()

    if not bcrypt.check_password_hash(business.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    sale = Sale.query.get(sale_id)

    if not sale:
        return jsonify({"message": "Not found"}), 404

    if business.id != sale.business_id:
        return jsonify({"message": "Not allowed"}), 400

    db.session.delete(sale)
    db.session.commit()

    return jsonify({"message": "Sale deleted"})
