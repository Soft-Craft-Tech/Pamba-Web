import json
import uuid
import logging
from datetime import datetime, date as dt_date, time as dt_time
from flask_mail import Message
from API import mail, db
from API.models import FailedNotification
from flask import render_template


def log_failed_notification(recipient, notification_type, message_params, error):
    """
    Log a failed notification to the database.
    """
    try:
        failed_notification = FailedNotification(
            id=str(uuid.uuid4()),
            recipient=recipient,
            notification_type=notification_type,
            message_params=json.dumps(message_params),
            error_message=str(error)
        )
        db.session.add(failed_notification)
        db.session.commit()
    except Exception as e:
        logging.error(f"Failed to log notification error: {e}")

def send_otp(recipient, otp, name):
    """
        Send account verification OTP
        :param recipient: Recipient Email
        :param name: Client name
        :param otp: OTP value
        :return: None
    """
    try:
        message = Message("[Action Required]: Verify Account - PAMBA", sender="pamba.africa", recipients=[recipient])
        message.html = render_template("otp.html", name=name, code=otp)
        mail.send(message)
    except:
        return False
    else:
        return True


def send_reset_email(recipient, token, name):
    """
        Send password reset token for businesses
        :param recipient: User Email
        :param token: JWT Token
        :param name: User's name
        :return:
    """
    try:
        reset_url = f"https://www.pamba.africa/reset-password/{token}"
        message = Message("Reset Password - PAMBA", sender="pamba.africa", recipients=[recipient])
        message.html = render_template("reset.html", url=reset_url, name=name)
        mail.send(message)
    except Exception:
        return False
    else:
        return True


def sent_client_reset_token(recipient: str, url: str, name: str) -> None:
    """
        Send password reset token for clients
        :param recipient: User Email
        :param url: Reset URL
        :param name: User's name
        :return: None
    """
    try:
        message = Message("Reset Password - PAMBA", sender="pamba.africa", recipients=[recipient])
        message.html = render_template("clientReset.html", url=url, name=name)
        mail.send(message)
    except:
        return False
    else:
        return True


def business_account_activation_email(recipient: str, token: str, name: str) -> None:
    """
        Send the account verification URL to businesses upon account creation.
        :param recipient: Recipient Email Address.
        :param token: Verification Token.
        :param name: Business Name.
        :return:
    """
    try:
        url = f"https://www.pamba.africa/verify/{token}"
        message = Message("[Action Required]: Activate your Pamba account", sender="pamba.africa", recipients=[recipient])
        message.html = render_template("activatebusiness.html", name=name, url=url)
        mail.send(message)
    except Exception:
        return False
    else:
        return True


def appointment_confirmation_email(
    client_name,
    appointment_date,
    appointment_time,
    service,
    business_name,
    business_address,
    latitude,                 
    longitude,               
    place_id,
    recipient
):
    """
    Send email notification for successful appointment booking
    """
    # Construct Google Maps Directions URL
    if latitude and longitude and place_id:
        directions_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}&query_place_id={place_id}"
    else:
        directions_url = "Location not available"
    
    date_str = appointment_date.isoformat() if isinstance(appointment_date, (datetime, dt_date)) else str(appointment_date)
    time_str = appointment_time.isoformat() if isinstance(appointment_time, (datetime, dt_time)) else str(appointment_time)

    try:
        message = Message("Pamba - New Appointment", sender="pamba.africa", recipients=[recipient])
        message.html = render_template(
            "confirmAppointment.html",
            name=client_name if client_name else None,
            appointment_date=date_str,
            service=service,
            appointment_time=time_str,
            business_name=business_name,
            business_address=business_address,
            business_direction=directions_url
        )
        mail.send(message) 
    except Exception as e:
        log_failed_notification(
            recipient=recipient,
            notification_type="appointment_confirmation",
            message_params={
                "client_name": client_name,
                "date": str(appointment_date),
                "time": str(appointment_time),
                "business_name": business_name,
                "business_address": business_address,
                "latitude": latitude,
                "longitude": longitude,
                "place_id": place_id
            },
            error=str(e)
        )
        return False
    else:
        return True


def send_ask_for_review_mail(url, name, business_name, recipient):
    """
        Ask clients to review
        :param url: Review url
        :param name: client name if any
        :param business_name: Name of Business
        :param recipient: Client Email
        :return:
    """
    try:
        message = Message("Pamba - Review your Appointment", sender="pamba.africa", recipients=[recipient])
        message.html = render_template(
            "askForReview.html",
            url=url,
            name=name,
            business_name=business_name
        )
        mail.send(message)
    except Exception as e:
        log_failed_notification(
            recipient=recipient,
            notification_type="ask_for_review",
            message_params={
                "url": url,
                "name": name,
                "business_name": business_name
            },
            error="Failed to send ask for review email"
        )
        return False 
    else:
        return True

