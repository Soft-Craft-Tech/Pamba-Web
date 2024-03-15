from flask_mail import Message
from API import mail


def send_otp(recipient, otp, name):
    """
        Send account verification OTP
        :param recipient: Recipient Email
        :param name: Client name
        :param otp: OTP value
        :return: None
    """
    message = Message("[Action Required]: Verify Account - PAMBA", sender="pamba.africa", recipients=[recipient])
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
    message = Message("Reset Password - PAMBA", sender="pamba.africa", recipients=[recipient])
    message.body = f"{name}, \n TOKEN: {token}"
    mail.send(message)


def business_account_activation_email(recipient, token, name):
    """
        Send the account verification URL to businesses upon account creation.
        :param recipient: Recipient Email Address.
        :param token: Verification Token.
        :param name: Business Name.
        :return:
    """
    message = Message("[Action Required]: Activate your Pamba account", sender="pamba.africa", recipients=[recipient])
    message.body = f"{name}, \nTOKEN: {token}"
    mail.send(message)
