from API.models import Appointment, Service
from flask import Blueprint, request, jsonify
from API.utilities.auth import client_login_required
from API import db
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
        return jsonify({"message": "Appoint doesn't exist"}), 404

    # Avoid Booking multiple appointments scheduled at the same time
    appointments_booked_same_time = Appointment.query.filter_by(date=date, time=time, client_id=client.id, cancelled=False).first()
    if appointments_booked_same_time:
        return jsonify({"message": "You have another appointment scheduled at this time."}), 400

    appointment.time = time
    appointment.date = date
    db.session.commit()

    return jsonify({"message": "Appointment has been rescheduled"}), 200
