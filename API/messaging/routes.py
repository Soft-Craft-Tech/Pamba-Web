from flask import Blueprint
from twilio.twiml.messaging_response import MessagingResponse

messaging_blueprint = Blueprint("messaging", __name__, url_prefix="/API/messaging")


@messaging_blueprint.route("/whatsapp-response", methods=["POST", "GET"])
def whatsapp_response():
    """
        Whatsapp message response when someone texts our number
        :return:
    """

    response = MessagingResponse()
    response.message("Thank you for contacting Pamba Africa. \nOur staff will respond to you shortly 😊")
    return str(response)
