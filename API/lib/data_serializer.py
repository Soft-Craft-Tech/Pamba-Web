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
        "verified": fields.Boolean,
        "dob": fields.DateTime(dt_format='iso8601'),
        "profile_image": fields.String
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
        "slug": fields.String,
        "email": fields.String,
        "phone": fields.String,
        "city": fields.String,
        "description": fields.String,
        "place_id": fields.String,
        "formatted_address": fields.String,
        "latitude": fields.Float,
        "longitude": fields.Float,
        "active": fields.Boolean,
        "verified": fields.Boolean,
        "join_date": fields.DateTime(dt_format='iso8601'),
        "rating": fields.String,
        "profile_img": fields.String,
        "weekday_opening": fields.String,
        "weekday_closing": fields.String,
        "weekend_opening": fields.String,
        "weekend_closing": fields.String,
        "profile_completed":fields.Boolean
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
        "create_at": fields.DateTime(dt_format='iso8601'),
        "completed": fields.Boolean,
        "service_id": fields.Integer
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
        "sent_at": fields.DateTime(dt_format='iso8601'),
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
        "id": fields.Integer,
        "payment_method": fields.String,
        "description": fields.String,
        "date_created": fields.DateTime(dt_format='iso8601')
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
        "description": fields.String,
        "business_id": fields.Integer,
        "service_category": fields.Integer,
        "price": fields.Integer,
        "estimated_service_time": fields.Float
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
        "created_at": fields.DateTime(dt_format='iso8601'),
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
        "updated_at": fields.DateTime(dt_format='iso8601')
     }

    return marshal(inventory, inventory_fields)


def serialize_review(review):
    """
        Serialize the business review.
        :param review: Review
        :return: Serialized object
    """
    review_fields = {
        "id": fields.Integer,
        "message": fields.String,
        "reviewed_at": fields.DateTime(dt_format='iso8601')
    }

    return marshal(review, review_fields)


def serialize_staff(staff):
    """
        Serialize the staff query object
        :param staff: Staff Object
        :return: JSON Serialized object
    """
    staff_fields = {
        "id": fields.Integer,
        "f_name": fields.String,
        "phone": fields.String,
        "created_at": fields.DateTime(dt_format='iso8601'),
        "role": fields.String,
        "public_id": fields.String
    }
    return marshal(staff, staff_fields)


def serialize_business_category(category):
    """
        Serialize Business Category
        :param category: Category object
        :return:Json
    """
    category_fields = {
        "id": fields.Integer,
        "category_name": fields.String
    }

    return marshal(category, category_fields)


def serialize_availability(availability):
    """
        Serialize staff availability
        :param availability: Availability Object
        :return: JSON serialized object
    """
    availability_fields = {
        "id": fields.Integer,
        "date": fields.DateTime(dt_format='iso8601'),
        "day_of_week": fields.Integer,
        "start_time": fields.String,
        "end_time": fields.String
    }
    return marshal(availability, availability_fields)


def serialize_gallery(gallery):
    """
        Serialize Gallery
        :param gallery: Gallery DB Object
        :return: Serialized gallery object
    """
    gallery_fields = {
        "id": fields.Integer,
        "created_at": fields.DateTime(dt_format='iso8601'),
        "image_url": fields.String,
        "business_id": fields.Integer
    }

    return marshal(gallery, gallery_fields)
