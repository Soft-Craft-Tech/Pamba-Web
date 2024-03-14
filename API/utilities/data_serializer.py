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
