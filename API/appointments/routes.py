from API.models import Appointment, Service
from flask import Blueprint, request, jsonify
from API.utilities.auth import client_login_required
from API import db

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
    new_appointment = Appointment(
        data=payload["date"],
        time=payload["time"],
        comment=payload["comment"].strip(),
        business_id=payload["provider"],
        client_id=client.id
    )
    for service_id in payload["services"]:
        service = Service.query.filter_by(id=service_id).first()
        if not service:
            return jsonify({"message": "Service not found"}), 404
        new_appointment.services.append(service)
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify("Booking Successful"), 200
