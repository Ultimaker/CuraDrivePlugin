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

from curaDrivePlugin.AuthorizationHelpers import AuthorizationHelpers
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

    # Emit signal when authentication is completed.
    onAuthenticated = Signal()

    def __init__(self):
        self._web_server = None  # type: HTTPServer
        self._web_server_thread = None  # type: threading.Thread
        self._user_profile_data = {}
        self._access_token_data = {}

    def getUserProfile(self) -> dict:
        """
        Get the user data that is stored in the JWT token.
        :return: Dict containing some user data.
        """
        return self._user_profile_data

    def getAccessToken(self) -> dict:
        """
        Get the access token response data.
        :return: Dict containing token data.
        """
        return self._access_token_data

    def startAuthorizationFlow(self) -> None:
        """Start a new OAuth2 authorization flow."""
        
        Logger.log("d", "Starting new OAuth2 flow...")
        
        # Create the tokens needed for the code challenge (PKCE) extension for OAuth2.
        # This is needed because the CuraDrivePlugin is a untrusted (open source) client.
        # More details can be found at https://tools.ietf.org/html/rfc7636.
        verification_code = AuthorizationHelpers.generateVerificationCode()
        challenge_code = AuthorizationHelpers.generateVerificationCodeChallenge(verification_code)
        
        # Create the query string needed for the OAuth2 flow.
        query_string = urlencode({
            "client_id": Settings.CLIENT_ID,
            "redirect_uri": Settings.CALLBACK_URL,
            "scope": "user.read",
            "response_type": "code",
            "state": "CuraDriveIsAwesome",
            "code_challenge": challenge_code,
            "code_challenge_method": "S512"
        })
        
        # Open the authorization page in a new browser window.
        webbrowser.open_new("{}?{}".format(self.AUTH_URL, query_string))
        
        # Start a local web server to receive the callback URL on.
        self._startWebServer(verification_code)

    def _startWebServer(self, code_verifier: str) -> None:
        """Start the local web server to handle the authorization callback."""
        
        Logger.log("i", "Starting local web server to handle authorization callback on port %s", self.PORT)
        
        # Create the server and inject the callback and code.
        self._web_server = AuthorizationRequestServer(("0.0.0.0", self.PORT), AuthorizationRequestHandler)
        self._web_server.setAuthorizationCallback(self._onAuthenticated)
        self._web_server.setCodeVerifier(code_verifier)
        
        # Start the server on a new thread.
        self._web_server_thread = threading.Thread(None, self._web_server.serve_forever)
        self._web_server_thread.start()

    def _stopWebServer(self) -> None:
        """Stop the web server if it was running. Also deletes the objects."""
        if self._web_server:
            self._web_server.server_close()
        self._web_server = None
        self._web_server_thread = None

    def _onAuthenticated(self, auth_response: dict) -> None:
        """Callback method for a successful authentication flow."""
        self._access_token_data = auth_response
        self.onAuthenticated.emit(auth_response)
        self._stopWebServer()
