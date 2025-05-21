from flask import Blueprint, jsonify, request
from API.lib.auth import verify_api_key, business_login_required, business_verification_required
from API.models import Business, BusinessGallery
from API.lib.data_serializer import serialize_gallery
from API import db

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

    images = business.gallery.order_by(BusinessGallery.created_at.desc()).all()
    serialized_images = [serialize_gallery(gallery) for gallery in images]

    return jsonify({"gallery": serialized_images}), 200


@gallery_blueprint.route("/add", methods=["POST"])
@business_login_required
@business_verification_required
def add_gallery_image(business):
    """
        Add Images to business Gallery
        :param business: Business logged-in
        :return: 404, 200
    """
    payload = request.get_json()
    image_url = payload["imgURL"]

    image = BusinessGallery(
        image_url=image_url,
        business_id=business.id
    )
    db.session.add(image)
    db.session.commit()

    return jsonify({"message": "Image Added"}), 200


@gallery_blueprint.route("/delete/<int:image_id>", methods=["DELETE"])
@business_login_required
def delete_gallery_image(business, image_id):
    """
        Delete an image from business gallery
        :param business: Logged-in Business
        :param image_id: ID of Image to be deleted
        :return: 400, 404, 200
    """

    image = BusinessGallery.query.get(image_id)
    if not image:
        return jsonify({"message": "Image doesn't exist"}), 404

    if image.business.id != business.id:
        return jsonify({"message": "Not allowed"}), 400

    db.session.delete(image)
    db.session.commit()

    return jsonify({"message": "Image deleted"}), 200
