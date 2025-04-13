import requests
from dotenv import load_dotenv
import os

load_dotenv()
URL: str = os.getenv("REMINDER_URL")
HEADERS: dict = {
    "X-API-KEY": os.getenv("API_KEY"),
    "Content-Type": "application/json"
}


def send_appointment_remainders() -> requests.Response:
    """
        Send notification to the client on the day of the appointment
        :return: None
    """

    response: requests.Response = requests.get(url=URL, headers=HEADERS)
    return response


if __name__ == "__main__":
    send_appointment_remainders()
