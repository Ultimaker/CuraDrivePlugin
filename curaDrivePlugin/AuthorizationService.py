# Copyright (c) 2017 Ultimaker B.V.
import random
import threading
import webbrowser
from _sha512 import sha512
from base64 import b64encode
from http.server import HTTPServer
from urllib.parse import urlencode

from UM.Logger import Logger
from UM.Signal import Signal
from curaDrivePlugin.AuthorizationRequestServer import AuthorizationRequestServer
from curaDrivePlugin.Settings import Settings
from curaDrivePlugin.AuthorizationRequestHandler import AuthorizationRequestHandler


class AuthorizationService:
    """
    The authorization service is responsible for handling the login flow,
    storing user credentials and providing account information.
    """

    AUTH_URL = "{}/authorize".format(Settings.OAUTH_SERVER_URL)

    PORT = Settings.CALLBACK_PORT

    onAuthenticated = Signal()

    def __init__(self):
        self._web_server = None  # type: HTTPServer
        self._web_server_thread = None  # type: threading.Thread
        self._user_profile_data = {
            "username": "chris",
            "avatar_url": "https://avatars3.githubusercontent.com/u/1134120?s=400&u=fe77552dc88f20e71d85826c36a4e36f123df5f8&v=4",
            "scopes": ["user.read", "backups.read", "backups.write"]
        }
        self._access_token_data = {}

    def getUserProfile(self) -> dict:
        return self._user_profile_data

    def getAccessToken(self) -> dict:
        return self._access_token_data

    def startAuthorizationFlow(self) -> None:
        code_verifier, code_challenge = self._generateVerificationToken()
        query = urlencode({
            "client_id": Settings.CLIENT_ID,
            "redirect_uri": Settings.CALLBACK_URL,
            "scope": "user.read",
            "response_type": "code",
            "state": "CuraDriveIsAwesome",
            "code_challenge": code_challenge,
            "code_challenge_method": "S512"
        })
        webbrowser.open_new("{}?{}".format(self.AUTH_URL, query))
        self._startWebServer(code_verifier)

    def _startWebServer(self, code_verifier: str) -> None:
        Logger.log("i", "Starting local web server to handle authorization callback on port %s", self.PORT)
        self._web_server = AuthorizationRequestServer(("0.0.0.0", self.PORT), AuthorizationRequestHandler)
        self._web_server.setAuthorizationCallback(self._onAuthenticated)
        self._web_server.setCodeVerifier(code_verifier)
        self._web_server_thread = threading.Thread(None, self._web_server.serve_forever)
        self._web_server_thread.start()

    def _stopWebServer(self) -> None:
        if self._web_server:
            self._web_server.server_close()
        self._web_server = None
        self._web_server_thread = None

    def _onAuthenticated(self, auth_response: dict) -> None:
        self._access_token_data = auth_response
        self.onAuthenticated.emit(auth_response)
        self._stopWebServer()

    def _parseJWT(self, jwt_token) -> dict:
        pass

    @staticmethod
    def _generateVerificationToken() -> (str, str):
        original = "".join(random.choice('0123456789ABCDEF') for i in range(16))
        input_bytes = original.encode()
        output_bytes = sha512(input_bytes).digest()
        verified = b64encode(output_bytes, altchars=b"_-").decode()
        return original, verified
