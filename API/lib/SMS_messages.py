from datetime import time


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
    message: str = f"""
Hello {name},
Your {service} appointment at {business} has been rescheduled to {date_} at {time_}.

Thank you.
Pamba Africa
"""

    return message
