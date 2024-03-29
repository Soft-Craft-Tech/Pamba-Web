from flask import jsonify, request, Blueprint
from API.models import Review, Business
from API import db
from API.lib.auth import client_login_required

reviews_blueprint = Blueprint("reviews", __name__, url_prefix="/API/reviews")


@reviews_blueprint.route("/create", methods=["POST"])
@client_login_required
def create_review(client):
    """
        Add reviews to businesses
        :param client: Client posting the review
        :return: 200
    """

    payload = request.get_json()
    message = payload["message"].strip()
    business_id = payload["businessID"]

    business = Business.query.get(business_id)
    if not business:
        return jsonify({"message": "Business doesn't exist"}), 404

    review = Review(
        message=message,
        business_id=business_id,
        client_id=client.id
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review has been posted"}), 200
