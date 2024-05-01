from datetime import timedelta, datetime, date


def add_decimal_hours_to_time(base_time, decimal_hours):
    """
        Add time give hours in decimals
        :param base_time: Initial time
        :param decimal_hours: Hour to be added
        :return: New Time
    """
    # Convert decimal hours to hours and minutes
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)

    # Create a timedelta object with the calculated hours and minutes
    time_delta = timedelta(hours=hours, minutes=minutes)

    # Add the timedelta to the base time
    new_time = (datetime.combine(date.today(), base_time) + time_delta).time()

    return new_time
