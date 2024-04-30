from API import db, bcrypt
from API.models import Staff
from flask import jsonify, Blueprint, request
from API.lib.auth import business_login_required, verify_api_key
from API.lib.data_serializer import serialize_staff
import secrets

staff_blueprint = Blueprint("staff", __name__, url_prefix="/API/staff")


@staff_blueprint.route("/create_staff", methods=["POST"])
@business_login_required
def add_staff(business):
    """
        Create new staff by the business owner
        :param business: Business owner
        :return: 409, 400, 201
    """
    payload = request.get_json()
    f_name = payload["f_name"].strip().title()
    l_name = payload["l_name"].strip().title()
    phone = payload["phone"]
    role = payload["role"].strip().title()
    public_id = secrets.token_hex(6)

    phone_exists = Staff.query.filter_by(phone=phone).first()
    if phone_exists:
        return jsonify({"message": "Phone number already exists"}), 409

    # Ensure the random public_id generated doesn't exist in the database
    public_id_exists = True
    while public_id_exists:
        staff_with_id = Staff.query.filter_by(public_id=public_id).first()
        if staff_with_id:
            public_id = secrets.token_hex(6)
        else:
            public_id_exists = False

    staff = Staff(
        f_name=f_name,
        l_name=l_name,
        phone=phone,
        role=role,
        public_id=public_id,
        employer_id=business.id
    )
    db.session.add(staff)
    db.session.commit()

    return jsonify({"message": "Staff Created", "staff": serialize_staff(staff)}), 201


@staff_blueprint.route("/delete-staff/<int:staff_id>", methods=["DELETE"])
@business_login_required
def delete_staff(business, staff_id):
    """
        Delete Staff
        :param business: Logged-in USER
        :param staff_id: Staff ID
        :return: 404, 401, 200
    """
    payload = request.get_json()
    password = payload["password"].strip()

    if not bcrypt.check_password_hash(business.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    if business.id != staff.employer_id:
        jsonify({"message": "Not allowed"}), 401

    db.session.delete(staff)
    db.session.commit()

    return jsonify({"message": "Staff deleted", "staff": serialize_staff(staff)}), 200


@staff_blueprint.route("/update-staff/<int:staff_id>", methods=["PUT"])
@business_login_required
def update_staff(business, staff_id):
    """
        Update the staff info
        :param business: Logged-In Business
        :param staff_id: ID of staff being updated
        :return: 200, 404, 401
    """
    payload = request.get_json()
    password = payload["password"].strip()
    phone = payload["phone"]
    role = payload["role"].strip().title()

    if not bcrypt.check_password_hash(business.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    if business.id != staff.employer_id:
        jsonify({"message": "Not allowed"}), 401

    # Check if the phone number is taken
    phone_exists = Staff.query.filter_by(phone=phone).first()
    if phone_exists and phone_exists.id != staff.id:
        return jsonify({"message": "Phone number already exists"}), 409

    staff.phone = phone
    staff.role = role
    db.session.commit()

    return jsonify({"message": "Updated", "staff": serialize_staff(staff)}), 200


@staff_blueprint.route("/single/<int:staff_id>", methods=["GET"])
@business_login_required
def fetch_single_staff(business, staff_id):
    """
        Get staff info for a single staff
        :param business: Logged-in Business
        :param staff_id: ID of the staff being fetched
        :return: 200, 401, 404
    """
    staff = Staff.query.get(staff_id)

    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    if staff.employer_id != business.id:
        return jsonify({"message": "Not Allowed"}), 401

    return jsonify({"staff": serialize_staff(staff)}), 200


@staff_blueprint.route("/all", methods=["GET"])
@business_login_required
def fetch_all_staff(business):
    """
        Fetch all staff associated with the business logged in
        :param business: Business logged in.
        :return: 200
    """
    all_staff = []
    staff_records = business.staff.all()

    for staff in staff_records:
        all_staff.append((serialize_staff(staff)))

    return jsonify({"staff": all_staff})
