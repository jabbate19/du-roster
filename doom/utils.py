from functools import wraps
from flask import session


def google_user_auth(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        uid = str(session["userinfo"].get("sub", ""))
        last = str(session["userinfo"].get("family_name", ""))
        first = str(session["userinfo"].get("given_name", ""))
        email = str(session["userinfo"].get("email", ""))
        auth_dict = {
            "first": first,
            "last": last,
            "uid": uid,
            "email": email,
        }
        kwargs["auth_dict"] = auth_dict
        return func(*args, **kwargs)
    return wrapped_function


def latin_to_utf8(string):
    return str(bytes(string, encoding='latin1'), encoding='utf8')
