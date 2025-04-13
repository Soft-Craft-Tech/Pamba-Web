from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os


def whatsapp_appointment_reminder(recipient, business, service, date, time):
    """
        Remind the client of their upcoming appointment via whatsapp
        :param recipient: Client's whatsapp number
        :param business: The shop where the appointment is booked
        :param service: Appointment service
        :param date: Appointment Date
        :param time: Appointment time
        :return:
    """
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER")
    message = f"""
Hello there 👋,\n
Just a friendly reminder about your upcoming {service} appointment with {business} on {date.strftime("%d-%b-%Y")} at {time.strftime("%I:%M %p")}.
Thank you.
\nRegards,
Pamba Africa
    """
    client = Client(account_sid, auth_token)
    try:
        client.messages.create(
            body=message,
            from_=twilio_number,
            to="whatsapp:"+recipient
        )
    except TwilioRestException:
        return False
    else:
        return True
