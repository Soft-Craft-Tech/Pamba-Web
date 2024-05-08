from datetime import timedelta


def format_date(date):
    """
        Format the date into this format for react scheduler: Mon May 06 2024 09:00:35 GMT+0300 (East Africa Time)
        :param date: Date Being Formatted
        :return:
    """
    # Define the timezone abbreviation and offset (replace with your timezone information)
    timezone_abbr = "East Africa Time"
    timezone_offset = "+0300"

    # Calculate the GMT offset in hours and minutes
    gmt_offset_hours = int(timezone_offset[:3]) // 100
    gmt_offset_minutes = int(timezone_offset[:3]) % 100

    # Calculate the UTC time
    utc_time = date - timedelta(hours=gmt_offset_hours, minutes=gmt_offset_minutes)

    # Format the datetime object
    formatted_time = utc_time.strftime("%a %b %d %Y %H:%M:%S GMT") + timezone_offset + f" ({timezone_abbr})"
    return formatted_time
