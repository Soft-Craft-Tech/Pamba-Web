from flask import jsonify, request, Blueprint
from API.models import ClientNotification
from API.lib.auth import client_login_required
from API import db
from API.lib.data_serializer import serialize_notification

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


@notifications_blueprint.route("/client/read/<int:notification_id>", methods=["PUT"])
@client_login_required
def read_notification(client, notification_id):
    """
        Mark notification as read
        :param client: Notification recipient.
        :param notification_id: Notification ID
        :return: 200, 400
    """
    notification = ClientNotification.query.get(notification_id)

    if not notification:
        return jsonify({"message": "Notification Not Found"}), 404

    if notification.client_id != client.id:
        return jsonify({"message": "Not allowed"}), 400

    if notification.read:
        return jsonify({"message": "Notification is already Read"}), 400

    notification.read = True
    db.session.commit()

    return jsonify({"message": "Notification Read", "notification": serialize_notification(notification)}), 200


@notifications_blueprint.route("/client/delete/<int:notification_id>", methods=["DELETE"])
@client_login_required
def delete_notification(client, notification_id):
    """
        Delete Notification.
        :param client:
        :param notification_id:
        :return:
    """

    notification = ClientNotification.query.get(notification_id)
    if not notification:
        return jsonify({"message": "Not Found"}), 400

    if notification.client_id != client.id:
        return jsonify({"message": "Not Allowed"}), 400

    db.session.delete(notification)
    db.session.commit()

    return jsonify({"message": "Notification deleted", "notification": serialize_notification(notification)}), 200
