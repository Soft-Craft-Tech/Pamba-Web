from flask import request, jsonify
import os
from functools import wraps
import jwt


def verify_api_key(func):
    """
        This decorator function wraps the route function (func) to check for API key in request header.
        :param func: Route function
        :return: decorated function
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        api_key = None
        if "X-API-KEY" in request.headers:
            api_key = request.headers["X-API-KEY"]

        if not api_key:
            return jsonify({"message": "API KEY is missing"}), 401

        if api_key != os.environ.get("API_KEY"):
            return jsonify({"message": "Invalid API KEY"}), 401
        return func(*args, **kwargs)
    return decorated


def generate_token(expiry, email):
    """
        Generate JWT tokens
        :param expiry: Token expiry
        :param email: User email to be encoded
        :return: JWT token
    """
    token = jwt.encode(
        {
            "email": email,
            "exp": expiry
        },
        os.environ.get('SECRET'),
        algorithm="HS256"
    )
    return token
