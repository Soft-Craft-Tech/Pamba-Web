from flask import Blueprint, jsonify
from API.lib.auth import verify_api_key
from API.models import Business
from API.lib.data_serializer import serialize_gallery

gallery_blueprint = Blueprint("gallery", __name__, url_prefix="/API/gallery")


@gallery_blueprint.route("/<string:slug>", methods=["GET"])
@verify_api_key
def fetch_business_gallery(slug):
    """
        Fetch the business's gallery images
        :param slug: Business slug value
        :return:
    """

    business = Business.query.filter_by(slug=slug).first()

    if not business:
        return jsonify({"message": "Business doesn't exist"}), 404

    images = business.gallery.all()
    serialized_images = [serialize_gallery(gallery) for gallery in images]

    return jsonify({"gallery": serialized_images}), 200
