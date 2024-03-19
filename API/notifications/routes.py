from flask import jsonify, request, Blueprint
from API.models import ClientNotification
from API.lib.auth import client_login_required
from API import db

notifications_blueprint = Blueprint("notifications", __name__, url_prefix="/API/notifications")


# ------------------------- CLIENTS ------------------------------------- #

@notifications_blueprint.route("/client/add", methods=["POST"])
@client_login_required
def add_client_notification(client):
    """
        Create notifications for clients.
        :param client: Logged in client
        :return: 201
    """
    payload = request.get_json()
    title = payload["title"]
    message = payload["message"]

    notification = ClientNotification(
        title=title,
        message=message,
        client_id=client.id
    )
    db.session.add(notification)
    db.session.commit()

    return jsonify({"message": "Notification sent"}), 201
