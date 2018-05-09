# Copyright (c) 2018 Ultimaker B.V.
import json
import random
from _sha512 import sha512
from base64 import b64encode
from typing import Optional

import requests
import jwt

# As this module is specific for Cura plugins, we can rely on these imports.
from UM.Logger import Logger

# Plugin imports need to be relative to work in final builds.
from .models import AuthenticationResponse, UserProfile, OAuth2Settings


class AuthorizationHelpers:
    """Class containing several helpers to deal with the authorization flow."""

    def __init__(self, settings: "OAuth2Settings"):
        self._settings = settings
        self._token_url = "{}/token".format(self._settings.OAUTH_SERVER_URL)

    def getAccessTokenUsingAuthorizationCode(self, authorization_code: str, verification_code: str)->\
            Optional["AuthenticationResponse"]:
        """
        Request the access token from the authorization server.
        :param authorization_code: The authorization code from the 1st step.
        :param verification_code: The verification code needed for the PKCE extension.
        :return: An AuthenticationResponse object.
        """
        return self.parseTokenResponse(requests.post(self._token_url, data={
            "client_id": self._settings.CLIENT_ID,
            "redirect_uri": self._settings.CALLBACK_URL,
            "grant_type": "authorization_code",
            "code": authorization_code,
            "code_verifier": verification_code,
            "scope": self._settings.CLIENT_SCOPES
        }))

    def getAccessTokenUsingRefreshToken(self, refresh_token: str) -> Optional["AuthenticationResponse"]:
        """
        Request the access token from the authorization server using a refresh token.
        :param refresh_token:
        :return: An AuthenticationResponse object.
        """
        return self.parseTokenResponse(requests.post(self._token_url, data={
            "client_id": self._settings.CLIENT_ID,
            "redirect_uri": self._settings.CALLBACK_URL,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": self._settings.CLIENT_SCOPES
        }))

    @staticmethod
    def parseTokenResponse(token_response: "requests.request") -> Optional["AuthenticationResponse"]:
        """
        Parse the token response from the authorization server into an AuthenticationResponse object.
        :param token_response: The JSON string data response from the authorization server.
        :return: An AuthenticationResponse object.
        """
        token_data = None

        try:
            token_data = json.loads(token_response.text)
        except ValueError:
            Logger.log("w", "Could not parse token response data: %s", token_response.text)

        if not token_data:
            return AuthenticationResponse(success=False, err_message="Could not read response.")

        if token_response.status_code not in (200, 201):
            return AuthenticationResponse(success=False, err_message=token_data["error_description"])

        return AuthenticationResponse(success=True,
                                      token_type=token_data["token_type"],
                                      access_token=token_data["access_token"],
                                      refresh_token=token_data["refresh_token"],
                                      expires_in=token_data["expires_in"],
                                      scope=token_data["scope"])

    def getPublicKeyJWT(self) -> Optional[str]:
        """
        Get the public key to decode the JWT.
        :return: The public key as string.
        """
        key_request = requests.get("{}/public-key".format(self._settings.OAUTH_SERVER_URL))
        if key_request.status_code not in (200, 201):
            Logger.log("w", "Could not retrieve public key from auth server: %s", key_request.text)
            return None
        return key_request.text

    @staticmethod
    def parseJWT(token: str, public_key: str) -> Optional["UserProfile"]:
        """
        Decode the JWT token to get the profile info.
        :param token: The encoded JWT token.
        :param public_key: The public key to decode with.
        :return: Dict containing some profile data.
        """
        try:
            jwt_data = jwt.decode(token, public_key, algorithms=["RS512"])
            return UserProfile(user_id = jwt_data["user_id"],
                               username = jwt_data["username"],
                               profile_image_url = jwt_data["profile_image_url"])
        except jwt.exceptions.ExpiredSignatureError:
            Logger.log("d", "JWT token was expired, it should be refreshed.")
        except jwt.exceptions.InvalidTokenError as error:
            Logger.log("w", "JWT token was invalid: %s", error)
        return None

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
