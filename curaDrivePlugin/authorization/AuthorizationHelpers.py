# Copyright (c) 2017 Ultimaker B.V.
import random
from _sha512 import sha512
from base64 import b64encode
from typing import Optional


class BaseModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Authentication data template.
class AuthenticationResponse(BaseModel):
    """Data comes from the token response with success flag and error message added."""
    success = True  # type: bool
    token_type = None  # type: Optional[str]
    access_token = None  # type: Optional[str]
    refresh_token = None  # type: Optional[str]
    expires_in = None  # type: Optional[str]
    scope = None  # type: Optional[str]
    err_message = None  # type: Optional[str]


# Response status template.
class ResponseStatus(BaseModel):
    code = 200  # type: int
    message = ""  # type str


# Response data template.
class ResponseData(BaseModel):
    status = None  # type: Optional[ResponseStatus]
    data_stream = None  # type: bytes
    content_type = "text_html"  # type: str


# Possible HTTP responses.
HTTP_STATUS = {
    "OK": ResponseStatus(code=200, message="OK"),
    "NOT_FOUND": ResponseStatus(code=404, message="NOT FOUND")
}


class AuthorizationHelpers:
    """Class containing several helpers to deal with the authorization flow."""
    
    @staticmethod
    def parseJWT(jwt: str, public_key: str) -> Optional[dict]:
        # TODO: actually parse JWT.
        return {
            "username": "chris",
            "profile_image_url": "https://avatars3.githubusercontent.com/u/1134120?s=400&u=fe77552dc88f20e71d85826c36a4e36f123df5f8&v=4",
            "scopes": ["user.read", "backups.read", "backups.write"],
            "exp": ""
        }

    @staticmethod
    def generateVerificationCode(code_length: int = 16) -> str:
        """
        Generate a 16-character verification code.
        :param code_length:
        :return:
        """
        return "".join(random.choice("0123456789ABCDEF") for i in range(code_length))

    @staticmethod
    def generateVerificationCodeChallenge(verification_code: str) -> str:
        """
        Generates a base64 encoded sha512 encrypted version of a given string.
        :param verification_code:
        :return: The encrypted code in base64 format.
        """
        encoded = sha512(verification_code.encode()).digest()
        return b64encode(encoded, altchars = b"_-").decode()
