def check_business_closed(time, date, business):
    """
        Check if the business will be closed at the time of the booking
        :param time: Time of the appointment booked
        :param date:  Date of the appointment
        :param business: The business being booked to.
        :return: True if the business is open else False
    """
    day_of_week = date.weekday()
    if day_of_week >= 5:  # is weekend
        if business.weekend_closing > time > business.weekend_opening:
            return True
    elif day_of_week < 5:
        if business.weekday_closing > time > business.weekday_opening:
            return True
    return False
