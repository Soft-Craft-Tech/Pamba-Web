from typing import Any

import requests
import json
import os


def send_sms(phone: str, message: str) -> object:
    """
        Send Mobile SMS
        :param phone: Recipient Phone Number
        :param message: Message being sent
        :return: None
    """
    url: str = 'https://isms.celcomafrica.com/api/services/sendsms/'
    headers: dict = {'Content-Type': 'application/json'}

    post_data: dict = {
        'partnerID': os.getenv("CELCOM_PARTNER_ID"),
        'apikey':  os.getenv("CELCOM_API_KEY"),
        'mobile': phone,
        'message': message,
        'shortcode': os.getenv("CELCOM_SHORTCODE"),
        'pass_type': 'plain'
    }

    payload: Any = json.dumps(post_data)
    response: Any = requests.post(url, headers=headers, data=payload)

    return response
