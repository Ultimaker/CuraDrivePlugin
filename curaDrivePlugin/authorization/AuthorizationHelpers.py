# Copyright (c) 2017 Ultimaker B.V.
import random
from _sha512 import sha512
from base64 import b64encode


class AuthorizationHelpers:
    
    @staticmethod
    def parseJWT(jwt: str) -> dict:
        return {
            "username": "chris",
            "avatar_url": "https://avatars3.githubusercontent.com/u/1134120?s=400&u=fe77552dc88f20e71d85826c36a4e36f123df5f8&v=4",
            "scopes": ["user.read", "backups.read", "backups.write"]
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
