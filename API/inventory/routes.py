from API import db, bcrypt
from flask import jsonify, Blueprint, request
from API.models import Inventory
from API.lib.auth import business_login_required
from API.lib.data_serializer import serialize_inventory
from datetime import datetime

inventory_blueprint = Blueprint("inventory", __name__, url_prefix="/API/inventory")


@inventory_blueprint.route("/record-inventory", methods=["POST"])
@business_login_required
def record_inventory(business):
    """
        Record new inventory
        :param business:
        :return: 201
    """
    payload = request.get_json()
    product = payload["product"].strip().title()

    new_inventory = Inventory(
        product=product,
        business_id=business.id
    )
    db.session.add(new_inventory)
    db.session.commit()

    return jsonify({"message": "Inventory created", "inventory": serialize_inventory(new_inventory)}), 201


@inventory_blueprint.route("/delete-inventory/<int:inventory_id>", methods=["DELETE"])
@business_login_required
def delete_inventory(business, inventory_id):
    """
        Delete Inventory with ID
        :param business:
        :param inventory_id: ID of the inventory to be deleted
        :return: 404, 401, 200
    """
    inventory = Inventory.query.get(inventory_id)
    if not inventory:
        return jsonify({"message": "Record not found"}), 404

    if inventory.business_id != business.id:
        return jsonify({"message": "Not Allowed"}), 403

    db.session.delete(inventory)
    db.session.commit()

    return jsonify({"message": "Deleted", "inventory": serialize_inventory(inventory)}), 200


@inventory_blueprint.route("/update-status/<int:inventory_id>", methods=["PUT"])
@business_login_required
def update_inventory_status(business, inventory_id):
    """
        Update the inventory level.
        :param business: Business logged in
        :param inventory_id: ID of inventory to be deleted
        :return: 404, 401, 400, 200
    """
    allowed_status = ("Critical", "Low", "Normal")
    payload = request.get_json()
    status = payload["status"].title().strip()

    if status not in allowed_status:
        return jsonify({"message": "Status not recognized"}), 400

    inventory = Inventory.query.get(inventory_id)
    if not inventory:
        return jsonify({"message": "Record not found"}), 404

    if inventory.business_id != business.id:
        return jsonify({"message": "Not allowed"}), 403

    inventory.status = status
    inventory.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"message": "Updated", "inventory": serialize_inventory(inventory)}), 200


@inventory_blueprint.route("/business-inventory", methods=["GET"])
@business_login_required
def fetch_all_records(business):
    """
        Fetch all inventory records for the business
        :param business:
        :return: 200
    """

    inventory_records = Inventory.query.filter_by(business_id=business.id).all()
    inventory = []

    for record in inventory_records:
        inventory.append(serialize_inventory(record))

    return jsonify({"inventory": inventory}), 200
