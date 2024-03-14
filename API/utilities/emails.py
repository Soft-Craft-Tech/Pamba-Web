from flask_mail import Message
from API import mail


def send_otp(recipient, otp):
    """
        Send password reset email
        :param recipient: Recipient Email
        :param otp: OTP value
        :return: None
    """
    message = Message("Your OTP", sender="communication@mykinyozi.com", recipients=[recipient])
    message.body = otp
    mail.send(message)
