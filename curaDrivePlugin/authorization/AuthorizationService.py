# Copyright (c) 2017 Ultimaker B.V.
import json
import threading
import webbrowser
from http.server import HTTPServer
from typing import Optional
from urllib.parse import urlencode

from UM.Logger import Logger
from UM.Preferences import Preferences
from UM.Signal import Signal

from curaDrivePlugin.Settings import Settings
from curaDrivePlugin.authorization.AuthorizationHelpers import AuthorizationHelpers, AuthenticationResponse
from curaDrivePlugin.authorization.AuthorizationRequestServer import AuthorizationRequestServer
from curaDrivePlugin.authorization.AuthorizationRequestHandler import AuthorizationRequestHandler


class AuthorizationService:
    """
    The authorization service is responsible for handling the login flow,
    storing user credentials and providing account information.
    """
    
    AUTH_DATA_PREFERENCE_KEY = "cura_drive_plugin/manual_instances"

    AUTH_URL = "{}/authorize".format(Settings.OAUTH_SERVER_URL)

    PORT = Settings.CALLBACK_PORT

    # Emit signal when authentication is completed.
    onAuthenticated = Signal()
    onAuthenticationError = Signal()

    def __init__(self):
        self._web_server = None  # type: HTTPServer
        self._web_server_thread = None  # type: threading.Thread
        self._auth_data = None  # type: AuthenticationResponse
        self._cura_preferences = Preferences.getInstance()
        self._loadAuthData()

    def getUserProfile(self) -> Optional[dict]:
        """
        Get the user data that is stored in the JWT token.
        :return: Dict containing some user data.
        """
        if not self._auth_data:
            return None
        return AuthorizationHelpers.parseJWT(self._auth_data.access_token)

    def getAccessToken(self) -> Optional[str]:
        """
        Get the access token response data.
        :return: Dict containing token data.
        """
        if not self._auth_data:
            return None
        return self._auth_data.access_token
    
    def deleteAuthData(self):
        """Delete authentication data from preferences and locally."""
        self._storeAuthData()
        self.onAuthenticated.emit()

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

    def _startWebServer(self, verification_code: str) -> None:
        """Start the local web server to handle the authorization callback."""

        Logger.log("d", "Starting local web server to handle authorization callback on port %s", self.PORT)
        
        # Create the server and inject the callback and code.
        self._web_server = AuthorizationRequestServer(("0.0.0.0", self.PORT), AuthorizationRequestHandler)
        self._web_server.setAuthorizationCallback(self._onAuthenticated)
        self._web_server.setVerificationCode(verification_code)
        
        # Start the server on a new thread.
        self._web_server_thread = threading.Thread(None, self._web_server.serve_forever)
        self._web_server_thread.start()

    def _stopWebServer(self) -> None:
        """Stop the web server if it was running. Also deletes the objects."""

        Logger.log("d", "Stopping local web server...")
        
        if self._web_server:
            self._web_server.server_close()
        self._web_server = None
        self._web_server_thread = None

    def _onAuthenticated(self, auth_response: "AuthenticationResponse") -> None:
        """Callback method for a successful authentication flow."""
        if auth_response.success:
            self._storeAuthData(auth_response)
            self.onAuthenticated.emit()
        else:
            self.onAuthenticationError.emit(auth_response.err_message)
        self._stopWebServer()  # Stop the web server at all times.

    def _loadAuthData(self) -> None:
        """Load authentication data from preferences if available."""
        self._cura_preferences.addPreference(self.AUTH_DATA_PREFERENCE_KEY, "{}")  # Ensure the preference exists.
        try:
            preferences_data = json.loads(self._cura_preferences.getValue(self.AUTH_DATA_PREFERENCE_KEY))
            self._profile_data = AuthenticationResponse(**preferences_data)
            self.onAuthenticated.emit()
        except ValueError as err:
            Logger.log("w", "Could not load auth data from preferences: %s", err)

    def _storeAuthData(self, profile_data: Optional["AuthenticationResponse"] = None) -> None:
        """Store authentication data in preferences and locally."""
        self._profile_data = profile_data
        if profile_data:
            self._cura_preferences.setValue(self.AUTH_DATA_PREFERENCE_KEY, json.dumps(profile_data.__dict__))
        else:
            self._cura_preferences.resetPreference(self.AUTH_DATA_PREFERENCE_KEY)
