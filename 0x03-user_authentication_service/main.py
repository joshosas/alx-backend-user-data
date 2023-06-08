#!/usr/bin/env python3
"""A basic end-to-end Integration Test for 'app.py'.
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test for registering a user.
    """
    url = f"{BASE_URL}/users"
    body = {
        'email': email,
        'password': password,
    }
    resp = requests.post(url, data=body)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "user created"}
    resp = requests.post(url, data=body)
    assert resp.status_code == 400
    assert resp.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test for attempting to login with a wrong password.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    resp = requests.post(url, data=body)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests logging in.
    """
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    resp = requests.post(url, data=body)
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "logged in"}
    return resp.cookies.get('session_id')


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
