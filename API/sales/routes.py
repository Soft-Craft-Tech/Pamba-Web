from datetime import datetime, timedelta, date
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

    sales: list = Sale.query.filter_by(business_id=business.id).all()
    all_sales: list = []

    for sale in sales:
        sale_info = serialize_sale(sale)
        sale_info["service"] = sale.service.service
        sale_info["service_id"] = sale.service.id
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

    sale = Sale.query.get(sale_id)

    if not sale:
        return jsonify({"message": "Not found"}), 404

    if business.id != sale.business_id:
        return jsonify({"message": "Not allowed"}), 400

    db.session.delete(sale)
    db.session.commit()

    return jsonify({"message": "Sale deleted"})


@sales_blueprint.route("/analysis", methods=["GET"])
@business_login_required
def revenue_analytics(business):
    """
        Business Revenue Analysis
        :param business: Logged in Business
        :return: 200
    """
    today: date = datetime.today().date()
    current_month: int = today.month
    current_year: int = today.year
    sales: list = business.sales.all()
    seven_days_ago: date = today - timedelta(days=7)

    lifetime_sales: list = []
    total_sales: int = 0
    current_month_revenue: int = 0
    last_seven_days_sales: int = 0

    for sale in sales:
        service: Service = sale.service
        serialized_sale: dict = serialize_sale(sale)
        serialized_sale["price"] = service.price
        serialized_sale["service_id"] = service.id
        lifetime_sales.append(serialized_sale)
        total_sales += service.price
        if sale.date_created.date().month == current_month and sale.date_created.date().year == current_year:
            current_month_revenue += service.price
        if sale.date_created.date() > seven_days_ago:
            last_seven_days_sales += service.price

    return jsonify(
        {
            "message": "Success",
            "lifetime_sales": lifetime_sales,
            "total_sales": total_sales,
            "current_month_revenue": current_month_revenue,
            "last_seven_days": last_seven_days_sales
        }
    ), 200


@sales_blueprint.route("/edit/<int:sale_id>", methods=["PUT"])
@business_login_required
def edit_sale(business, sale_id):
    """
        Edit a sale
        :param business : Business
        :param sale_id : ID of the sale to edit 
        :return : 200, 400 , 404
    """
    payload = request.get_json()
    payment_method = payload.get("paymentmethod", "").strip().title()
    description = payload.get("description", "").strip().capitalize()
    service_id = payload.get("service_id")

    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({"message": "Sale not found"}), 404
    
    if business.id != sale.business_id:
        return jsonify({"message": "Not found"}), 400
    
    if payment_method:
        sale.payment_method = payment_method
    
    if description:
        sale.description = description
    
    if service_id:
        business_services = [service.id for service in business.services.all()]
        if service_id not in business_services:
            return jsonify({"message": "Service does not exist!"}), 400
        sale.service_id = service_id
    
    db.session.commit()

    return jsonify({"message": "Sale updated", "updatedSale": serialize_sale(sale)}), 200
