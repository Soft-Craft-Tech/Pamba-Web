from API import db
from API.lib.utils import add_decimal_hours_to_time
from API.models import Staff, Appointment, StaffAvailability, Business
from flask import jsonify, Blueprint, request
from API.lib.auth import business_login_required, verify_api_key, business_verification_required
from API.lib.data_serializer import serialize_staff
import secrets
from datetime import datetime

staff_blueprint = Blueprint("staff", __name__, url_prefix="/API/staff")


@staff_blueprint.route("/create_staff", methods=["POST"])
@business_login_required
@business_verification_required
def add_staff(business):
    """
        Create new staff by the business owner
        :param business: Business owner
        :return: 409, 400, 201
    """
    try:
        # TODO: decorator to make sure business is verified
        payload = request.get_json()
        f_name = payload["f_name"].strip().title()
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
            phone=phone,
            role=role,
            public_id=public_id,
            employer_id=business.id
        )
        db.session.add(staff)
        db.session.commit()
        return jsonify({"message": "Staff Created", "staff": serialize_staff(staff)}), 201
    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Failed to create staff due to an unexpected issue"}), 400


@staff_blueprint.route("/delete-staff/<int:staff_id>", methods=["DELETE"])
@business_login_required
@business_verification_required
def delete_staff(business, staff_id):
    """
        Delete Staff
        :param business: Logged-in USER
        :param staff_id: Staff ID
        :return: 404, 401, 200
    """
    try:
        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({"message": "Staff not found"}), 404

        if business.id != staff.employer_id:
            jsonify({"message": "Not allowed"}), 401

        db.session.delete(staff)
        db.session.commit()
        return jsonify({"message": "Staff deleted", "staff": serialize_staff(staff)}), 200
    except Exception:
        db.session.rollback() 
        return jsonify({"message": "Failed to delete staff due to an unexpected issue"}), 400


@staff_blueprint.route("/update-staff/<int:staff_id>", methods=["PUT"])
@business_login_required
@business_verification_required
def update_staff(business, staff_id):
    """
        Update the staff info
        :param business: Logged-In Business
        :param staff_id: ID of staff being updated
        :return: 200, 404, 401
    """
    try:
        payload = request.get_json()
        phone = payload["phone"]
        role = payload["role"].strip().title()
        
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

    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Failed to update staff due to an unexpected issue"}), 400


@staff_blueprint.route("/single/<int:staff_id>", methods=["GET"])
@business_login_required
def fetch_single_staff(business, staff_id):
    """
        Get staff info for a single staff
        :param business: Logged-in Business
        :param staff_id: ID of the staff being fetched
        :return: 200, 401, 404
    """
    try:
        staff = Staff.query.get(staff_id)

        if not staff:
            return jsonify({"message": "Staff not found"}), 404

        if staff.employer_id != business.id:
            return jsonify({"message": "Not Allowed"}), 401
        return jsonify({"staff": serialize_staff(staff)}), 200
    except Exception:
        return jsonify({"message": "Failed to fetch staff due to an unexpected issue"}), 400


@staff_blueprint.route("/all/<string:slug>", methods=["GET"])
@verify_api_key
def fetch_all_staff(slug):
    """
        Fetch all staff associated with the business logged in
        :param slug: Slug of the business
        :return: 200
    """
    try:
        all_staff = []
        business = Business.query.filter_by(slug=slug).first()

        for staff in business.staff.order_by(Staff.f_name).all():
            all_staff.append((serialize_staff(staff)))
        return jsonify({"staff": all_staff})
    except Exception:
        return jsonify({"message": "Failed to fetch staff due to an unexpected issue"}), 400


@staff_blueprint.route("/unavailability/<int:staff_id>", methods=["GET"])
@verify_api_key
def fetch_staff_unavailability(staff_id):
    """
        Check when a staff is available for booking
        :param staff_id: ID of staff being requested
        :return: 404, 400, 200
    """
    try:
        payload = request.get_json()
        date = datetime.strptime(payload["date"], '%d-%m-%Y').date()
        time = datetime.strptime(payload["time"], '%H:%M').time()

        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({"message": "Staff not found"}), 404

        staff_unavailability = staff.availability.filter_by(date=date).all()
        staff_appointments = staff.appointments.filter(Appointment.date >= date).all()

        if staff_unavailability:
            for period in staff_unavailability:
                if period.end_time > time > period.start_time:
                    return jsonify({"message": "Staff not Available at this time"}), 400

        for appointment in staff_appointments:
            # Add the estimated time it takes to complete the services
            appointment_completion_time = appointment.service[0].estimated_service_time  # How long an appointment takes
            appointment_finish_time = add_decimal_hours_to_time(appointment.time, float(appointment_completion_time))

            if appointment_finish_time > time > appointment.time:
                return jsonify({"message": "Staff is booked at this time"}), 400
        return jsonify({"message": "Staff is available"}), 200
    except Exception:
        return jsonify({"message": "Failed to check staff availability due to an unexpected issue"}), 400


@staff_blueprint.route("/create-unavailability/<int:staff_id>", methods=["POST"])
@business_login_required
@business_verification_required
def add_staff_unavailability(business, staff_id):
    """
        Add staff unavailability periods to prevent booking.
        :param business: Logged-in business.
        :param staff_id: ID of staff.
        :return: 201 on success, 400 for invalid input
    """
    try:
        payload = request.get_json()
        date = datetime.strptime(payload["date"], '%d-%m-%Y').date()
        all_day = payload["all_day"]
        day_of_week = date.weekday()

        if date < datetime.today().date():
            return jsonify({"message": "Date must be today or in the future"}), 400

        staff = Staff.query.get(staff_id)
        if not staff:
            return jsonify({"message": "Staff not found"}), 404

        if staff.business.id != business.id:
            return jsonify({"message": "Unauthorized: Not allowed to manage this staff"}), 401

        if all_day:
            opening_time = business.weekend_opening if day_of_week >= 5 else business.weekday_opening
            closing_time = business.weekend_closing if day_of_week >= 5 else business.weekday_closing
            if not (opening_time and closing_time):
                return jsonify({"message": "Business hours not set for this day"}), 400

            availability = StaffAvailability(
                date=date,
                day_of_week=day_of_week,
                staff_id=staff.id,
                start_time=opening_time,
                end_time=closing_time
            )
            db.session.add(availability)
        else:
            periods = payload["periods"]
            if not periods:
                return jsonify({"message": "At least one unavailability period required if not all_day"}), 400

            for period in periods:
                try:
                    start_time_str = period["startTime"]
                    end_time_str = period["endTime"]
                except KeyError as e:
                    return jsonify({"message": f"Invalid period: '{e.args[0]}' key is required"}), 400

                try:
                    start_time = datetime.strptime(start_time_str, '%H:%M').time()
                    end_time = datetime.strptime(end_time_str, '%H:%M').time()
                except ValueError:
                    return jsonify({"message": "Invalid time format in period. Use HH:MM (00:00-23:59)"}), 400

                if start_time >= end_time:
                    return jsonify({"message": "End time must be after start time in period"}), 400

                availability = StaffAvailability(
                    date=date,
                    day_of_week=day_of_week,
                    staff_id=staff.id,
                    start_time=start_time,
                    end_time=end_time
                )
                db.session.add(availability)

        db.session.commit()
        return jsonify({"message": "Staff unavailability added successfully"}), 201

    except KeyError as e:
        return jsonify({"message": f"Invalid payload: '{e.args[0]}' key is required"}), 400
    except ValueError:
        return jsonify({"message": "Invalid date format. Use DD-MM-YYYY"}), 400
    except AttributeError:
        return jsonify({"message": "Invalid payload: JSON format required"}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Failed to add unavailability due to an unexpected issue"}), 400