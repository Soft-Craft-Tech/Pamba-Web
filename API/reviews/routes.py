from flask import jsonify, request, Blueprint
from API.models import Review, Appointment
from API import db
from API.lib.auth import client_login_required

reviews_blueprint = Blueprint("reviews", __name__, url_prefix="/API/reviews")


@reviews_blueprint.route("/create/<int:appointment_id>", methods=["POST"])
def create_review(appointment_id):
    """
        Add reviews to businesses.
        :param appointment_id: ID of Appointment being reviewed.
        :return: 200
    """

    payload = request.get_json()
    message = payload["message"].strip()

    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        return jsonify({"message": "Appointment doesn't exist"}), 404

    review = Review(
        message=message,
        business_id=appointment.business.id,
        client_id=appointment.client_id,
        appointment_id=appointment.id
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review has been posted"}), 200
