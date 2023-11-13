from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, Query, Request
from pydantic import BaseModel, ValidationError

app = FastAPI(
    title="WattTime Data API",
    version="V3",
    servers=[{"url": "https://api.watttime.org", "description": "WattTime Base API"}],
    description="To start using the API, first register for an account by using the /register endpoint. Then use the /login endpoint to obtain an access token. You can then use your token to access the remainder of our endpoints. You must include your token in an authorization (bearer) header in subsequent requests to retrieve data. Your access token will expire after 30 minutes and you'll need to sign in again to obtain a new one.",
)

PARAM_USER: str = Query(
    description="name of user that will be used in subsequent calls",
    example="freddo",
)
PARAM_PASSWORD: str = Query(
    description="user password. Password must be at least 8 characters, with at least 1 of each alpha, number and special characters.",
    example="the_frog",
)
PARAM_EMAIL: str = Query(
    description="valid email address. The email address used to register will only be used for communication regarding API outages and updates. The email address will not be shared or used for any other promotional purpose. For others in your organization who would like these updates, they can subscribe to our Status Page. ",
    example="freddo@frog.org",
)
PARAM_ORG: Optional[str] = Query(
    description="organization name",
    example="freds world",
    default=None,
)


REGISTER_EXAMPLE = """
# To register, use the code below. Please note that for these code examples we are using filler values for username
# (freddo), password (the_frog), email (freddo@frog.org), org (freds world) and you should replace each if you are
# copying and pasting this code.

import requests
register_url = 'https://api2.watttime.org/v2/register'
params = {'username': 'freddo',
         'password': 'the_frog',
         'email': 'freddo@frog.org',
         'org': 'freds world'}
rsp = requests.post(register_url, json=params)
print(rsp.text)
"""

LOGIN_EXAMPLE = """
# To login and obtain an access token, use this code:

import requests
from requests.auth import HTTPBasicAuth
login_url = 'https://api.watttime.org/login'
rsp = requests.get(login_url, auth=HTTPBasicAuth('freddo', 'the_frog'))
print(rsp.json())
"""

PASSWORD_EXAMPLE = """
# To reset your password, use this code:

import requests
password_url = 'https://api.watttime.org/password/?username=freddo'
rsp = requests.get(password_url)
print(rsp.json())
"""


class RegisterResponse(BaseModel):
    user: str
    ok: str

    class Config:
        json_schema_extra = {"example": {"user": "freddo", "ok": "User created"}}


class LoginResponse(BaseModel):
    token: str

    class Config:
        json_schema_extra = {"example": {"token": "abcdef0123456789fedcabc"}}


class PasswordResponse(BaseModel):
    ok: str

    class Config:
        json_schema_extra = {
            "example": {"ok": "Please check your email for the password reset link"}
        }


@app.post(
    "/register",
    summary="Provide basic information to self register for an account.",
    tags=["Authenticate"],
    response_model=RegisterResponse,
    openapi_extra={
        "x-codeSamples": [
            {
                "lang": "Python",
                "source": REGISTER_EXAMPLE,
                "label": "Python",
            }
        ]
    },
)
def post_username(
    request: Request,
    username: str = PARAM_USER,
    password: str = PARAM_PASSWORD,
    email: str = PARAM_EMAIL,
    org: Optional[str] = PARAM_ORG,
) -> RegisterResponse:
    return


@app.get(
    "/login",
    summary="Use HTTP basic auth to exchange username and password for an access token.",
    description="Remember that you need to include this token in an authorization bearer header for all subsequent data calls. This header has the form: `Authorization: Bearer <your_token>`",
    tags=["Authenticate"],
    response_model=LoginResponse,
    openapi_extra={
        "x-codeSamples": [
            {
                "lang": "Python",
                "source": REGISTER_EXAMPLE,
                "label": "Python",
            }
        ]
    },
)
def get_token(
    request: Request,
) -> LoginResponse:
    return


@app.get(
    "/password",
    summary="Provide your username to request an email be sent to you with password reset instructions.",
    tags=["Authenticate"],
    response_model=PasswordResponse,
    openapi_extra={
        "x-codeSamples": [
            {
                "lang": "Python",
                "source": PASSWORD_EXAMPLE,
                "label": "Python",
            }
        ]
    },
)
def get_password(
    request: Request,
    username: str = PARAM_USER,
) -> PasswordResponse:
    return
