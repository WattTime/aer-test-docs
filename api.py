from typing import Any, Dict, Literal, Optional

from fastapi import FastAPI, Query, Request
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, EmailStr


def get_markdown(_filename: str):
    with open(_filename, "r") as _f:
        return _f.read()


app = FastAPI(
    title="WattTime Data API",
    version="V3",
    servers=[{"url": "https://api.watttime.org", "description": "WattTime Base API"}],
    openapi_tags=[
        {
            "name": "Introduction",
            "description": get_markdown("introduction.md"),
        },
        {
            "name": "Authentication",
            "description": "To start using the API, first register for an account by using the /register endpoint. Then use the /login endpoint to obtain an access token. You can then use your token to access the remainder of our endpoints. You must include your token in an authorization (bearer) header in subsequent requests to retrieve data. Your access token will expire after 30 minutes and you'll need to sign in again to obtain a new one.",
        },
        {"name": "GET Forecast"},
        {"name": "GET Historical"},
        {"name": "Signal access"},
        {"name": "Regions and Maps"},
        {
            "name": "Transitioning from v2 to v3",
            "description": get_markdown("transition.md"),
        },
        {
            "name": "Technical Support",
            "description": get_markdown("tech-support.md"),
        },
    ],
)

PARAM_USER: str = Query(
    description="name of user that will be used in subsequent calls",
    example="freddo",
)
PARAM_PASSWORD: str = Query(
    description="user password. Password must be at least 8 characters, with at least 1 of each alpha, number and special characters.",
    example="the_frog",
)
PARAM_EMAIL: EmailStr = Query(
    description="valid email address. The email address used to register will only be used for communication regarding API outages and updates. The email address will not be shared or used for any other promotional purpose. For others in your organization who would like these updates, they can subscribe to our Status Page. ",
    example="freddo@frog.org",
)
PARAM_ORG: Optional[str] = Query(
    description="organization name",
    example="freds world",
    default=None,
)
PARAM_SIGNAL_TYPE: Literal["co2_moer", "co2_aoer", "health_damage"] = Query(
    description="signal_type for which to look up region",
    example="co2_moer",
)
PARAM_LONGITUDE: float = Query(
    description="Longitude of desired location",
    example=42.372,
)
PARAM_LATITUDE: float = Query(
    description="Latitude of desired location",
    example=-72.519,
)


REGISTER_EXAMPLE = """
# To register, use the code below. Please note that for these code examples we are using filler values for username
# (freddo), password (the_frog), email (freddo@frog.org), org (freds world) and you should replace each if you are
# copying and pasting this code.

import requests
register_url = 'https://api.watttime.org/register'
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

REGION_LOC_EXAMPLE = """
# Make sure to replace the parameters username (e.g. ‘freddo’) and password (e.g. ‘the_frog’) with your registered
# credentials when using this code. You should not add in your token here. The code automatically generates a new token
# each time you run it.


import requests
from requests.auth import HTTPBasicAuth

login_url = 'https://api.watttime.org/login'
token = requests.get(login_url, auth=HTTPBasicAuth(‘freddo’, ‘the_frog’)).json()['token']

region_url = 'https://api.watttime.org/v3/region-from-loc'
headers = {'Authorization': 'Bearer {}'.format(token)}
params = {'latitude': '42.372', 'longitude': '-72.519', 'signal_type': 'co2_moer'}
rsp=requests.get(region_url, headers=headers, params=params)
print(rsp.text)
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


class RegionLocResponse(BaseModel):
    abbrev: str
    name: str
    signal_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "abbrev": "ISONE_WCMA",
                "name": "ISONE Western/Central Massachusetts",
                "signal_type": "co2_moer",
            }
        }


@app.post(
    "/register",
    summary="Register New User",
    description="Provide basic information to self register for an account.",
    tags=["Authentication"],
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
    email: EmailStr = PARAM_EMAIL,
    org: Optional[str] = PARAM_ORG,
) -> RegisterResponse:
    return


@app.get(
    "/login",
    summary="Login & Obtain Token",
    description="Use HTTP basic auth to exchange username and password for an access token. Remember that you need to include this token in an authorization bearer header for all subsequent data calls. This header has the form: `Authorization: Bearer <your_token>`",
    tags=["Authentication"],
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
    summary="Password Reset",
    description="Provide your username to request an email be sent to you with password reset instructions.",
    tags=["Authentication"],
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


@app.get(
    "/v3/region-from-loc",
    summary="Determine Grid Region",
    description="Emissions intensity varies by location, specifically the location where an energy-using device is interconnected to the grid. This endpoint, provided with latitude and longitude parameters, returns the details of the grid region serving that location, if known, or a Coordinates not found error if the point lies outside of known/covered regions.",
    tags=["Regions and Maps"],
    response_model=RegionLocResponse,
    openapi_extra={
        "x-codeSamples": [
            {
                "lang": "Python",
                "source": REGION_LOC_EXAMPLE,
                "label": "Python",
            }
        ]
    },
)
def get_reg_loc(
    request: Request,
    signal_type: Literal["co2_moer", "co2_aoer", "health_damage"] = PARAM_SIGNAL_TYPE,
    latitude: float = PARAM_LATITUDE,
    longitude: float = PARAM_LONGITUDE,
) -> RegionLocResponse:
    return
