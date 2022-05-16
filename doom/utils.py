from functools import wraps
from flask import session

RANK_LIST = [
        ("CMD", "COMMANDER DOOM"),
        ("XO", "EXECUTIVE OFFICER"),
        ("COL", "COLONEL"),
        ("LTC", "LIEUTENANT COLONEL"),
        ("MAJ", "MAJOR"),
        ("CPT", "CAPTAIN"),
        ("1stLT", "FIRST LIEUTENANT"),
        ("2ndLT", "SECOND LIEUTENANT"),
        ("SMB", "SERGEANT MAJOR OF THE BATTALION"),
        ("CSM", "COMMAND SERGEANT MAJOR"),
        ("SGM", "SERGEANT MAJOR"),
        ("1SG", "FIRST SERGEANT"),
        ("MSG", "MASTER SERGEANT"),
        ("SFC", "SERGEANT FIRST CLASS"),
        ("SSG", "STAFF SERGEANT"),
        ("SGT", "SERGEANT"),
        ("CPL", "CORPORAL"),
        ("LCPL", "LANCE CORPORAL"),
        ("PFC", "PRIVATE FIRST CLASS"),
        ("PVT", "PRIVATE")
    ]

RANK_VALUE = {
    "CMD": 18,
    "COL": 17,
    "LTC": 16,
    "MAJ": 15,
    "CPT": 14,
    "1stLT": 13,
    "2ndLT": 12,
    "SMB": 11,
    "CSM": 10,
    "SGM": 9,
    "1SG": 8,
    "MSG": 7,
    "SFC": 6,
    "SSG": 5,
    "SGT": 4,
    "CPL": 3,
    "LCPL": 2,
    "PFC": 1,
    "PVT":0
}

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
