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
        "google_map": fields.String,
        "active": fields.Boolean,
        "verified": fields.Boolean,
        "join_date": fields.DateTime
    }

    return marshal(business, business_fields)
