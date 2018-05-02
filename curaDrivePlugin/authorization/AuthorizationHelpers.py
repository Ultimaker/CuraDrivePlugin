# Copyright (c) 2018 Ultimaker B.V.
import json
import random
from _sha512 import sha512
from base64 import b64encode
from typing import Optional

import requests
import jwt

from UM.Logger import Logger
from curaDrivePlugin.Settings import Settings


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

    TOKEN_URL = "{}/token".format(Settings.OAUTH_SERVER_URL)
    OAUTH_GRANT_TYPE_AUTH_CODE = "authorization_code"
    OAUTH_GRANT_TYPE_REFRESH = "refresh_token"

    @classmethod
    def getAccessTokenUsingAuthorizationCode(cls, authorization_code: str, verification_code: str)->\
            Optional["AuthenticationResponse"]:
        """
        Request the access token from the authorization server.
        :param authorization_code: The authorization code from the 1st step.
        :param verification_code: The verification code needed for the PKCE extension.
        :return: An AuthenticationResponse object.
        """
        return cls.parseTokenResponse(requests.post(cls.TOKEN_URL, data={
            "client_id": Settings.CLIENT_ID,
            "redirect_uri": Settings.CALLBACK_URL,
            "grant_type": cls.OAUTH_GRANT_TYPE_AUTH_CODE,
            "code": authorization_code,
            "code_verifier": verification_code
        }))

    @classmethod
    def getAccessTokenUsingRefreshToken(cls, refresh_token: str) -> Optional["AuthenticationResponse"]:
        """
        Request the access token from the authorization server using a refresh token.
        :param refresh_token:
        :return: An AuthenticationResponse object.
        """
        return cls.parseTokenResponse(requests.post(cls.TOKEN_URL, data={
            "client_id": Settings.CLIENT_ID,
            "redirect_uri": Settings.CALLBACK_URL,
            "grant_type": cls.OAUTH_GRANT_TYPE_REFRESH,
            "refresh_token": refresh_token
        }))

    @staticmethod
    def parseTokenResponse(token_response: "requests.request") -> Optional["AuthenticationResponse"]:
        token_data = None

        try:
            token_data = json.loads(token_response.text)
        except ValueError as err:
            Logger.log("w", "Could not parse token response data: %s", err)

        if not token_data:
            return AuthenticationResponse(success=False, err_message="Could not read response.")

        if token_response.status_code != 200:
            return AuthenticationResponse(success=False, err_message=token_data["error_description"])

        return AuthenticationResponse(success=True,
                                      token_type=token_data["token_type"],
                                      access_token=token_data["access_token"],
                                      refresh_token=token_data["refresh_token"],
                                      expires_in=token_data["expires_in"],
                                      scope=token_data["scope"])

    @staticmethod
    def getPublicKeyJWT() -> Optional[str]:
        """
        Get the public key to decode the JWT.
        :return: The public key as string.
        """
        key_request = requests.get("{}/public-key".format(Settings.OAUTH_SERVER_URL))
        if key_request.status_code != 200:
            Logger.log("w", "Could not retrieve public key from authorization server: %s", key_request.text)
            return None
        return key_request.text

    @staticmethod
    def parseJWT(token: str, public_key: str) -> Optional[dict]:
        """
        Decode the JWT token to get the profile info.
        :param token: The encoded JWT token.
        :param public_key: The public key to decode with.
        :return: Dict containing some profile data.
        """
        return jwt.decode(token, public_key, algorithms=["RS512"])

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
