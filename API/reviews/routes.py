from flask import jsonify, request, Blueprint
import time
from API.lib.data_serializer import serialize_review
from API.models import Review, Appointment, Business
from API import db
from API.lib.auth import verify_api_key

reviews_blueprint = Blueprint("reviews", __name__, url_prefix="/API/reviews")


@reviews_blueprint.route("/create/<int:appointment_id>", methods=["POST"])
@verify_api_key
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


@reviews_blueprint.route("/all/<string:slug>", methods=["GET"])
@verify_api_key
def list_reviews(slug):
    """
        List Reviews for a give business slug
        :param slug: Business slug
        :return:
    """
    business = Business.query.filter_by(slug=slug).first()
    if not business:
        return jsonify({"message": "Shop doesn't exist"}), 400

    reviews = business.reviews.all()
    serialized_reviews = []
    for review in reviews:
        serializer = serialize_review(review)
        serializer["reviewer"] = review.client.name
        serializer["rating"] = 3
        serialized_reviews.append(serializer)

    return jsonify({"reviews": serialized_reviews}), 200


