from API.models import Appointment, Service, Staff
from flask import Blueprint, request, jsonify
from API.lib.auth import client_login_required, business_login_required
from API.lib.data_serializer import serialize_appointment
from API import db, bcrypt
from datetime import datetime

appointment_blueprint = Blueprint("appointments", __name__, url_prefix="/API/appointments")


@appointment_blueprint.route("/book", methods=["POST"])
@client_login_required
def book_appointment(client):
    """
        Book Appointment
        :param client: Logged in client
        :return: 200
    """
    payload = request.get_json()
    date = datetime.strptime(payload["date"], '%d-%m-%Y')
    time = datetime.strptime(payload["time"], '%H:%M').time()
    comment = payload["comment"].strip()
    business_id = payload["provider"]

    if not client.verified:
        return jsonify({"message": "Please, verify your account."}), 401

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

    for service_id in payload["services"]:
        service = Service.query.filter_by(id=service_id).first()
        if not service:
            return jsonify({"message": "Service not found"}), 404
        new_appointment.services.append(service)
    db.session.add(new_appointment)
    db.session.commit()
    # Send email or notification when a new appointment is scheduled

    return jsonify({"message": "Booking Successful"}), 200


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
        return jsonify({"message": "Not allowed"}), 401

    if appointment.completed:
        return jsonify({"message": "Appointment already completed."}), 400

    # Avoid Booking multiple appointments scheduled at the same time
    appointments_booked_same_time = Appointment.query\
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
        return jsonify({"message": "Not allowed"}), 401

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
            "last": sorted_previous[-1]
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
        return jsonify({"message": "Not allowed"}), 400

    if appointment.cancelled:
        return jsonify({"message": "This appointment was cancelled"}), 400

    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    if staff.employer_id != business.id:
        return jsonify({"message": "Not allowed"}), 400

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
