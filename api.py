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
    summary="If you're looking for the legacy APIv2 documentation, you'll find it [here](https://legacy-docs.watttime.org).",
    openapi_tags=[
        {
            "name": "Introduction",
            "description": get_markdown("introduction.md"),
        },
        {
            "name": "Authentication",
            "description": "To start using the API, first register for an account by using the `/register` endpoint. Then use the `/login` endpoint to obtain an access token. You can then use your token to access the remainder of our endpoints. You must include your token in an authorization (bearer) header in subsequent requests to retrieve data. Your access token will expire after 30 minutes and you'll need to sign in again to obtain a new one.",
        },
        {"name": "GET Account Access"},
        {"name": "GET Regions and Maps"},
        {"name": "GET Forecast"},
        {"name": "GET Historical"},
        {
            "name": "Transitioning from APIv2 to APIv3",
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
    description="valid email address. The email address used to register will only be used for communication regarding API outages and updates. The email address will not be shared or used for any other promotional purpose. For others in your organization who would like these updates, they can subscribe to our Status Page.",
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
import requests

url = "https://api.watttime.org/v3/region-from-loc"

# Provide your TOKEN here, see https://docs.watttime.org/#tag/Authentication/operation/get_token_login_get for more information
TOKEN = ""
headers = {"Authorization": f"Bearer {TOKEN}"}
params = {"latitude": "42.372", "longitude": "-72.519", "signal_type": "co2_moer"}
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
print(response.json())
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
    region: str
    region_full_name: str
    signal_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "region": "ISONE_WCMA",
                "region_full_name": "ISONE Western/Central Massachusetts",
                "signal_type": "co2_moer",
            }
        }


@app.post(
    "/register",
    summary="Register New User",
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
    """
    Provide basic information to self-register for an account.

    **Note:** The `/register` endpoint accepts the parameters in the body of the request. It does not accept them in the URL as a query string, because that isn't as secure. The input parameters should be included as a JSON object (in the body), as shown in the sample code on the right.
    """
    return


@app.get(
    "/login",
    summary="Login & Obtain Token",
    tags=["Authentication"],
    response_model=LoginResponse,
    openapi_extra={
        "x-codeSamples": [
            {
                "lang": "Python",
                "source": LOGIN_EXAMPLE,
                "label": "Python",
            }
        ]
    },
)
def get_token(
    request: Request,
) -> LoginResponse:
    """
    Use HTTP basic auth to exchange username and password for an access token. Remember that you need to include this token in an authorization bearer header for all subsequent data calls. This header has the form: `Authorization: Bearer <your_token>`

    **Note:** Token expires after 30 minutes. If a data call returns `HTTP 401` error code, you will need to call `/login` again to receive a new token.
    """
    return


@app.get(
    "/password",
    summary="Password Reset",
    description="Provide your `username` to request an email be sent to you with password reset instructions.",
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
    tags=["GET Regions and Maps"],
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
