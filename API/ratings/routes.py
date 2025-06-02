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
    try:
        payload = request.get_json()
        rating_value = payload.get("rating")
        business_id = payload.get("businessID")

        if rating_value is None or business_id is None:
            return jsonify({"message": "Missing rating or businessID in request"}), 200

        business = Business.query.get(business_id)
        if not business:
            return jsonify({"message": "Business doesn't exist"}), 200

        new_rating = Rating(
            rating=rating_value,
            business_id=business_id
        )

        db.session.add(new_rating)

        # Calculate updated business rating
        ratings = Rating.query.filter_by(business_id=business.id).all()
        if ratings:
            rating_score, _ = calculate_ratings(ratings=ratings, breakdown=True)
        else:
            rating_score = 0

        business.rating = rating_score
        db.session.commit()

        return jsonify({"message": "Rating has been posted"}), 200

    except Exception as e:
        print(f"[ERROR] Failed to post rating: {e}")
        return jsonify({"message": "Something went wrong while posting the rating"}), 200
