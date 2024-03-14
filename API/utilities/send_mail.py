from flask_mail import Message
from API import mail


def send_otp(recipient, otp, name):
    """
        Send password reset email
        :param recipient: Recipient Email
        :param name: User's name
        :param otp: OTP value
        :return: None
    """
    message = Message("Verify Account - PAMBA", sender="communication@mykinyozi.com", recipients=[recipient])
    message.body = f"{name}, \n OTP: {otp}"
    mail.send(message)


def send_reset_email(recipient, token, name):
    """
        Send password reset token
        :param recipient: User Email
        :param token: JWT Token
        :param name: User's name
        :return:
    """
    message = Message("Reset Password - PAMBA", sender="communication@mykinyozi.com", recipients=[recipient])
    message.body = f"{name}, \n TOKEN: {token}"
    mail.send(message)
