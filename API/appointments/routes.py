from API.models import Appointment, Service, Staff, Client, Business
from flask import Blueprint, request, jsonify
from API.lib.auth import client_login_required, business_login_required, verify_api_key
from API.lib.data_serializer import serialize_appointment
from API import db, bcrypt
from datetime import datetime
from API.lib.checkBusinessClosed import check_business_closed

appointment_blueprint = Blueprint("appointments", __name__, url_prefix="/API/appointments")


@appointment_blueprint.route("/book", methods=["POST"])
@client_login_required
def book_appointment(client):
    """
        Book Appointment from the mobile application
        :param client: Logged in client
        :return: 200
    """
    payload = request.get_json()
    date = datetime.strptime(payload["date"], '%d-%m-%Y')
    time = datetime.strptime(payload["time"], '%H:%M').time()
    comment = payload["comment"].strip()
    business_id = payload["provider"]
    service = payload["service"]

    if not client.verified:
        return jsonify({"message": "Please, verify your account."}), 403
    new_appointment = Appointment(
        date=date,
        time=time,
        comment=comment,
        business_id=business_id,
        client_id=client.id
    )
    # Avoid Booking multiple appointments scheduled at the same time
    appointment = Appointment.query.filter_by(date=date, time=time, client_id=client.id, cancelled=False).first()
    if appointment:
        return jsonify({"message": "You have another appointment scheduled at this time."}), 400

    service = Service.query.filter_by(id=service).first()
    if not service:
        return jsonify({"message": "Service not found"}), 404
    new_appointment.service_id = service.id
    db.session.add(new_appointment)
    db.session.commit()
    # Send email or notification when a new appointment is scheduled

    return jsonify({"message": "Booking Successful"}), 200


@appointment_blueprint.route("/book/web-appointments", methods=["POST"])
@verify_api_key
def book_appointment_on_web():
    """
        Book appointment from the web without Auth
        :return: 200, 404
    """
    payload = request.get_json()
    date = datetime.strptime(payload["date"], '%d-%m-%Y')
    time = datetime.strptime(payload["time"], '%H:%M').time()
    comment = payload["comment"].strip()
    business_id = payload["business"]
    service_id = payload["service"]
    staff_id = payload["staff"]
    email = payload["email"].strip().lower()
    phone = payload["phone"].strip()

    service = Service.query.get(service_id)
    if not service:
        return jsonify({"message": "The service you are booking is unavailable"}), 404

    business = Business.query.get(business_id)
    if not business:
        return jsonify({"message": "Business not found"}), 404

    # Check whether the business will be closed for the hours booked.
    open_status = check_business_closed(time, date, business)
    if not open_status:
        return jsonify({"message": "Our premises are not open at the picked time and day"}), 400

    # Check staff availability.
    if staff_id:
        staff = business.staff.filter_by(id=staff_id).first()
        if not staff:
            return jsonify({"message": "Staff you booked with doesn't exist"}), 404

        # Check if the staff is booked at the selected time slot
        current_date = datetime.now().date()
        upcoming_staffs_appointments = staff.appointments.filter(Appointment.date >= current_date).all()
        for appointment in upcoming_staffs_appointments:
            if appointment.date == date.date() and appointment.time == time:
                return jsonify({
                    "message": "The Staff you selected is already booked at this time. "
                               "Please book with a different staff or let us assign you someone"
                }
                ), 400

    client = Client.query.filter_by(email=email).first()
    # If the client is not a mobile user or hasn't booked an appointment before
    if not client:
        client = Client(
            email=email,
            phone=phone
        )
        db.session.add(client)

    appointment = Appointment(
        date=date,
        time=time,
        comment=comment,
        business_id=business.id,
        staff_id=staff_id if staff_id else None,
        client_id=client.id
    )
    db.session.add(appointment)
    service.appointments.append(appointment)
    db.session.commit()

    # Send Confirmation Notification/Email

    return jsonify({"message": "Appointment Booked Successfully"}), 201


@appointment_blueprint.route("/reschedule/<int:appointment_id>", methods=["PUT"])
@client_login_required
def reschedule_appointment(client, appointment_id):
    """
        Client reschedule appointment.
        :param client: Client
        :param appointment_id: ID of appointment being rescheduled
        :return: 200
    """

    payload = request.get_json()
    date = datetime.strptime(payload["date"], '%d-%m-%Y')
    time = datetime.strptime(payload["time"], '%H:%M').time()
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"message": "Appointment doesn't exist"}), 404

    if appointment.client_id != client.id:
        return jsonify({"message": "Not allowed"}), 403

    if appointment.completed:
        return jsonify({"message": "Appointment already completed."}), 400

    # Avoid Booking multiple appointments scheduled at the same time
    appointments_booked_same_time = Appointment.query \
        .filter_by(date=date, time=time, client_id=client.id, cancelled=False).first()
    if appointments_booked_same_time:
        return jsonify({"message": "You have another appointment scheduled at this time."}), 400

    appointment.time = time
    appointment.date = date
    db.session.commit()

    return jsonify({"message": "Appointment has been rescheduled"}), 200


@appointment_blueprint.route("/cancel/<int:appointment_id>", methods=["PUT"])
@client_login_required
def cancel_appointment(client, appointment_id):
    """
        Cancel appointment
        :param client: Logged in client
        :param appointment_id: ID of the appointment being cancelled
        :return: 200, 401
    """
    payload = request.get_json()
    comment = payload["comment"]
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({"message": "Appointment not Found"}), 404

    if appointment.client_id != client.id:
        return jsonify({"message": "Not allowed"}), 403

    if appointment.completed:
        return jsonify({"message": "Appointment already completed."}), 400

    appointment.cancelled = True
    if comment:
        appointment.comment = comment
    db.session.commit()

    return jsonify({"message": "Cancellation Successful"}), 200


@appointment_blueprint.route("/my-appointments", methods=["GET"])
@client_login_required
def my_appointments(client):
    """
        Fetch the client's appointments: Last appointment, upcoming
        :param client:
        :return:
    """
    appointments = Appointment.query.filter_by(client_id=client.id).order_by(Appointment.date.desc()).all()
    cancelled_appointments = []
    upcoming_appointments = []
    previous_appointments = []

    if not appointments:
        return jsonify({"message": "No appointments"}), 404

    for appointment in appointments:
        serialized_appointment = serialize_appointment(appointment)
        serialized_appointment["imgUrl"] = appointment.business.profile_img
        serialized_appointment["phone"] = appointment.business.phone
        serialized_appointment["name"] = appointment.business.business_name
        serialized_appointment["description"] = appointment.business.location
        serialized_appointment["mapUrl"] = appointment.business.google_map
        if appointment.cancelled:
            cancelled_appointments.append(serialized_appointment)
        if appointment.completed:
            previous_appointments.append(serialized_appointment)
        else:
            if not appointment.cancelled:
                upcoming_appointments.append(serialized_appointment)

    sorted_previous = sorted(previous_appointments, key=lambda x: x['id'])

    return jsonify(
        {
            "message": "Success",
            "cancelled": cancelled_appointments,
            "upcoming": upcoming_appointments,
            "previous": previous_appointments,
            "last": sorted_previous[-1] if len(sorted_previous) > 0 else None
        }
    ), 200


@appointment_blueprint.route("/assign-appointment/<int:appointment_id>", methods=["PUT"])
@business_login_required
def assign_appointment(business, appointment_id):
    """
        Assign an appointment to a member of staff to handle
        :param business: Logged-in business/owner
        :param appointment_id: Appointment being assigned
        :return: 404, 401, 400, 200
    """
    payload = request.get_json()
    staff_id = payload["staffID"]
    password = payload["password"]

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"message": "Not Found"}), 404

    if not bcrypt.check_password_hash(business.password, password):
        return jsonify({"message": "Incorrect Password"}), 401

    if appointment.business_id != business.id:
        return jsonify({"message": "Not allowed"}), 403

    if appointment.cancelled:
        return jsonify({"message": "This appointment was cancelled"}), 400

    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    if staff.employer_id != business.id:
        return jsonify({"message": "Not allowed"}), 403

    appointment.staff_id = staff.id
    return jsonify({"message": "Successful", "appointment": serialize_appointment(appointment)}), 200


@appointment_blueprint.route("/business-appointments", methods=["GET"])
@business_login_required
def fetch_business_appointments(business):
    """
        Fetch all appointments booked with the logged-in business
        :param business: Logged-in
        :return: 200
    """
    appointments = Appointment.query.filter_by(business_id=business.id).all()
    all_appointments = []

    for appointment in appointments:
        all_appointments.append(serialize_appointment(appointment))

    return jsonify({"appointment": all_appointments}), 200


@appointment_blueprint.route("/end_appointment/<int:appointment_id>", methods=["PUT"])
@business_login_required
def end_appointment(business, appointment_id):
    """
        End Appointment when completed
        Trigger a notification for appointment Review.
        :param business: Logged in Business.
        :param appointment_id: ID of appointment being ended
        :return: 200, 400.
    """

    appointment = Appointment.query.get(appointment_id)

    if appointment.business_id == business.id:
        return jsonify({"message": "Not Allowed"}), 400

    appointment.completed = True
    db.session.commit()

    return jsonify({"message": "Appointment Ended"}), 200
