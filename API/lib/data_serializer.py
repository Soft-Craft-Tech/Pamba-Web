from flask_restful import fields, marshal


def serialize_client(client):
    """
        Client's json serializer
        :param client: client object
        :return: client's json data
    """

    client_fields = {
        "id": fields.Integer,
        "name": fields.String,
        "email": fields.String,
        "phone": fields.String,
        "verified": fields.Boolean
    }

    return marshal(client, client_fields)


def serialize_business(business):
    """
        Serializer the business object
        :param business: Business Object
        :return: json serialized business info
    """
    business_fields = {
        "id": fields.Integer,
        "business_name": fields.String,
        "category": fields.String,
        "slug": fields.String,
        "email": fields.String,
        "phone": fields.String,
        "city": fields.String,
        "location": fields.String,
        "google_map": fields.Url,
        "active": fields.Boolean,
        "verified": fields.Boolean,
        "join_date": fields.DateTime
    }

    return marshal(business, business_fields)


def serialize_appointment(appointment):
    """
        Serializer for the appointment query objects
        :param appointment: Appointment object
        :return: serialized appointment data
    """
    appointment_fields = {
        "id": fields.Integer,
        "date": fields.String,
        "time": fields.String,
        "cancelled": fields.Boolean,
        "comment": fields.String,
        "create_at": fields.DateTime,
        "completed": fields.Boolean
    }

    return marshal(appointment, appointment_fields)


def serialize_notification(notification):
    """
        Serialize notification
        :param notification:
        :return: JSON serialized notification
    """

    notification_fields = {
        "id": fields.Integer,
        "message": fields.String,
        "title": fields.String,
        "sent_at": fields.DateTime,
        "read": fields.Boolean
    }
    return marshal(notification, notification_fields)


def serialize_sale(sale):
    """
        Serialize sales records
        :param sale:
        :return: JSON serialized sale record
    """
    sales_fields = {
        "payment_method": fields.String,
        "description": fields.String,
        "date_created": fields.DateTime
    }
    return marshal(sale, sales_fields)


def serialize_account(account):
    """
        Serialize expense accounts
        :param account:
        :return: JSON serialized account data
    """
    account_fields = {
        "account_name": fields.String,
        "description": fields.String,
        "id": fields.Integer,
        "business_id": fields.Integer
    }

    return marshal(account, account_fields)


def serialize_service(service):
    """
        Serialize services
        :param service:
        :return: Serialized service object
    """
    service_fields = {
        "id": fields.Integer,
        "service": fields.String,
        "description": fields.String
    }

    return marshal(service, service_fields)


def serialize_expenses(expense):
    """
        Serialize business expenses
        :param expense:
        :return: Serialized Expense
    """

    expense_fields = {
        "id": fields.Integer,
        "expense": fields.String,
        "amount": fields.Integer,
        "description": fields.String,
        "created_at": fields.DateTime,
        "expense_account": fields.Integer
    }

    return marshal(expense, expense_fields)


def serialize_inventory(inventory):
    """
        Serialize Business Inventory
        :param inventory:
        :return:
    """

    inventory_fields = {
        "id": fields.Integer,
        "product": fields.String,
        "status": fields.String,
        "updated_at": fields.DateTime
     }

    return marshal(inventory, inventory_fields)
