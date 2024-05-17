from flask import jsonify, request, Blueprint

from API.lib.rating_calculator import calculate_ratings
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
    # Calculate the rating score for the business. Add to the Business's rating field.
    ratings = Rating.query.filter_by(business_id=business.id).all()
    if ratings:
        rating_score, _ = calculate_ratings(ratings=ratings, breakdown=True)
    else:
        rating_score = 0

    db.session.add(rating)
    business.rating = rating_score
    db.session.commit()

    return jsonify({"message": "Rating has been posted"}), 200
