from datetime import time, date


def reschedule_appointment_composer(name: str, time_: time, date_: str, service: str, business: str) -> str:
    """
        Compose Reschedule appointment SMS message
        :param name: Client Name
        :param time_: Appointment's New Time
        :param date_: Appointment's New Date
        :param service: Appointment's service
        :param business: The Business where the appointment is booked
        :return: Message
    """
    reschedule_message: str = f"""
Hello {name},
Your {service} appointment at {business} has been rescheduled to {date_} at {time_}.

Thank you.
Pamba Africa
"""

    return reschedule_message


def appointment_remainder_message(name: str, time_: time, date_: str, service: str, business: str) -> str:
    """
        Compose Reschedule appointment SMS message
        :param name: Client Name
        :param time_: Appointment's New Time
        :param date_: Appointment's New Date
        :param service: Appointment's service
        :param business: The Business where the appointment is booked
        :return: Message
    """
    message: str = f"""
Hello {name},
Reminder: You have a {service} appointment on {date_} at {time_} at {business}. See you there!

Thank you.
Pamba Africa
"""

    return message


def new_appointment_notification_message(name: str, time_: str, date_: str, service: str, business: str) -> str:
    """
        Compose SMS message for new appointment
        :param name: Client Name
        :param time_: Appointment Time
        :param date_: Appointment Date
        :param service: Service to Be offered
        :param business: Name of the Business
        :return:
    """
    message: str = f"""
Hello {name},
Your {service} appointment has been successfully booked at {business} on {date_} at {time_}.
We have sent the map directions to your email.
 
Thank you,
Pamba Africa.
    """
    return message
