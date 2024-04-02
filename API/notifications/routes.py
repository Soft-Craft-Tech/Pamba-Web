from flask import jsonify, request, Blueprint
from API.models import ClientNotification, BusinessNotification
from API.lib.auth import client_login_required, business_login_required
from API import db
from API.lib.data_serializer import serialize_notification

notifications_blueprint = Blueprint("notifications", __name__, url_prefix="/API/notifications")


# ------------------------- CLIENTS ------------------------------------- #

@notifications_blueprint.route("/client/add", methods=["POST"])
def add_client_notification():
    """
        Create notifications for clients.
        :return: 201
    """
    payload = request.get_json()
    title = payload["title"]
    message = payload["message"]
    client_id = payload["clientID"]

    notification = ClientNotification(
        title=title,
        message=message,
        client_id=client_id
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
        return jsonify({"message": "Not allowed"}), 403

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
        return jsonify({"message": "Not Allowed"}), 403

    db.session.delete(notification)
    db.session.commit()

    return jsonify({"message": "Notification deleted", "notification": serialize_notification(notification)}), 200


@notifications_blueprint.route("/client/all", methods=["GET"])
@client_login_required
def fetch_all(client):
    """
        Fetch all notifications
        :param client:
        :return: 200
    """
    notifications = ClientNotification.query.filter_by(client_id=client.id).all()
    all_notifications = []

    for notification in notifications:
        all_notifications.append(serialize_notification(notification))

    return jsonify({"notifications": all_notifications}), 200


# ------------------------------- BUSINESSES NOTIFICATIONS ---------------------------------------- #

@notifications_blueprint.route("/businesses/create", methods=["POST"])
def add_business_notification():
    """
        Create new notification for the Business
        :return: 201
    """
    payload = request.get_json()
    title = payload["title"]
    message = payload["message"]
    business_id = payload["businessID"]

    notification = BusinessNotification(
        title=title,
        message=message,
        business_id=business_id
    )
    db.session.add(notification)
    db.session.commit()

    return jsonify({"message": "Notification sent"}), 201


@notifications_blueprint.route("/business/read/<int:notification_id>", methods=["PUT"])
@business_login_required
def read_business_notification(business, notification_id):
    """
        Mark a notification as read
        :param business: Logged-in Business
        :param notification_id: Notification ID to be read
        :return: 404, 401, 200
    """
    notification = BusinessNotification.query.get(notification_id)

    if not notification:
        return jsonify({"message": "Not found"}), 404

    if notification.business_id != business.id:
        return jsonify({"message": "Not Allowed"}), 403

    if notification.read:
        return jsonify({"message": "Notification is already Read"}), 400

    notification.read = True
    db.session.commit()
    return jsonify({"message": "Notification Read", "notification": serialize_notification(notification)}), 200


@notifications_blueprint.route("/business/delete/<int:notification_id>", methods=["DELETE"])
@business_login_required
def delete_business_notification(business, notification_id):
    """
        Delete notification for Business
        :param business: Logged-In Business/Owner
        :param notification_id: ID of notification to be deleted
        :return: 200, 404
    """
    notification = BusinessNotification.query.get(notification_id)

    if not notification:
        return jsonify({"message": "Not found"}), 404

    if notification.business_id != business.id:
        return jsonify({"message": "Not Allowed"}), 403

    db.session.delete(notification)
    db.session.commit()

    return jsonify({"message": "Deleted", "notification": serialize_notification(notification)}), 200
