import pyotp
from API import bcrypt


def generate_otp():
    """
        Generate an OTP the hash it, for clients to veirfy their accounts with.
        :return: OTP, OTP Secret
    """
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    hashed_otp = bcrypt.generate_password_hash(otp).decode("utf-8")

    return otp, hashed_otp

