from flask import jsonify, request, Blueprint
from API.models import Rating, Business
from API import db
from API.lib.auth import verify_api_key

ratings_blueprint = Blueprint("rating", __name__, url_prefix="/API/ratings")


@ratings_blueprint.route("/new", methods=["POST"])
@verify_api_key
def add_rating():
    """
        Add rating to a business
        :return: 200
    """
    payload = request.get_json()
    rating = payload["rating"]
    business_id = payload["businessID"]

    business = Business.query.get(business_id)
    if not business:
        return jsonify({"message": "Business doesn't exist"}), 404

    rating = Rating(
        rating=rating,
        business_id=business_id
    )
    db.session.add(rating)
    db.session.commit()

    return jsonify({"message": "Rating has been posted"}), 200
