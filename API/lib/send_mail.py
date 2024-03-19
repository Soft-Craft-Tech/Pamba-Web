from flask_mail import Message
from API import mail
from flask import render_template
from API import create_app


def send_otp(recipient, otp, name):
    """
        Send account verification OTP
        :param recipient: Recipient Email
        :param name: Client name
        :param otp: OTP value
        :return: None
    """
    message = Message("[Action Required]: Verify Account - PAMBA", sender="pamba.africa", recipients=[recipient])
    message.html = render_template("otp.html", name=name, code=otp)
    mail.send(message)


def send_reset_email(recipient, token, name):
    """
        Send password reset token for businesses
        :param recipient: User Email
        :param token: JWT Token
        :param name: User's name
        :return:
    """
    reset_url = f"https://www.pamba.africa/reset/{token}"
    message = Message("Reset Password - PAMBA", sender="pamba.africa", recipients=[recipient])
    app = create_app()
    with app.open_resource("static/assets/logo.svg") as logo_file:
        message.attach("logo.svg", "image/svg", logo_file.read())

    message.html = render_template("reset.html", url=reset_url, name=name)
    mail.send(message)


def sent_client_reset_token(recipient, token, name):
    """
        Send password reset token for clients
        :param recipient: User Email
        :param token: JWT Token
        :param name: User's name
        :return:
    """
    message = Message("Reset Password - PAMBA", sender="pamba.africa", recipients=[recipient])
    app = create_app()
    with app.open_resource("static/assets/logo.svg") as logo_file:
        message.attach("logo.svg", "image/svg", logo_file.read())

    message.html = render_template("clientReset.html", token=token, name=name)
    mail.send(message)


def business_account_activation_email(recipient, token, name):
    """
        Send the account verification URL to businesses upon account creation.
        :param recipient: Recipient Email Address.
        :param token: Verification Token.
        :param name: Business Name.
        :return:
    """
    url = f"https://pamba.africa/activate/{token}"
    message = Message("[Action Required]: Activate your Pamba account", sender="pamba.africa", recipients=[recipient])
    app = create_app()
    with app.open_resource("static/assets/logo.svg") as logo_file:
        message.attach("logo.svg", "image/svg", logo_file.read())

    message.html = render_template("activatebusiness.html", name=name, url=url)
    mail.send(message)
