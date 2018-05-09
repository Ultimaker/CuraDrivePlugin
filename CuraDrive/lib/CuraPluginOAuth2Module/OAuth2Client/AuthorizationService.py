# Copyright (c) 2017 Ultimaker B.V.
import json
import threading
import webbrowser
from http.server import HTTPServer
from typing import Optional
from urllib.parse import urlencode

# As this module is specific for Cura plugins, we can rely on these imports.
from UM.Logger import Logger
from UM.Preferences import Preferences
from UM.Signal import Signal

# Plugin imports need to be relative to work in final builds.
from .AuthorizationHelpers import AuthorizationHelpers
from .AuthorizationRequestServer import AuthorizationRequestServer
from .AuthorizationRequestHandler import AuthorizationRequestHandler
from .models import OAuth2Settings, AuthenticationResponse, UserProfile


class AuthorizationService:
    """
    The authorization service is responsible for handling the login flow,
    storing user credentials and providing account information.
    """
    
    AUTH_DATA_PREFERENCE_KEY = "cura_drive_plugin/auth_data"

    # Emit signal when authentication is completed.
    onAuthStateChanged = Signal()

    # Emit signal when authentication failed.
    onAuthenticationError = Signal()

    def __init__(self, settings: "OAuth2Settings"):
        self._OAuth2Settings = OAuth2Settings
        self._auth_helpers = AuthorizationHelpers(settings)
        self._web_server = None  # type: Optional[HTTPServer]
        self._web_server_thread = None  # type: Optional[threading.Thread]
        self._web_server_port = self._OAuth2Settings.CALLBACK_PORT  # type: str
        self._auth_url = "{}/authorize".format(self._OAuth2Settings.OAUTH_SERVER_URL)
        self._auth_data = None  # type: Optional[AuthenticationResponse]
        self._user_profile = None  # type: Optional[UserProfile]
        self._cura_preferences = Preferences.getInstance()
        self._loadAuthData()

    def getUserProfile(self) -> Optional["UserProfile"]:
        """
        Get the user data that is stored in the JWT token.
        :return: Dict containing some user data.
        """
        if not self._user_profile:
            # If no user profile was stored locally, we try to get it from JWT.
            self._user_profile = self._parseJWT()

        if not self._user_profile:
            # If there is still no user profile from the JWT, we have to log in again.
            return None

        return self._user_profile

    def _parseJWT(self) -> Optional["UserProfile"]:
        """
        Tries to parse the JWT if all the needed data exists.
        :return: UserProfile if found, otherwise None.
        """
        if not self._auth_data:
            # If no auth data exists, we should always log in again.
            return None

        public_key = self._auth_helpers.getPublicKeyJWT()
        if not public_key:
            # If the public key wasn't found (e.g. not online), we cannot parse the JWT.
            return None

        user_data = self._auth_helpers.parseJWT(self._auth_data.access_token, public_key)
        if user_data:
            # If the profile was found, we return it immediately.
            return user_data

        # The JWT was expired or invalid and we should request a new one.
        self._auth_data = self._auth_helpers.getAccessTokenUsingRefreshToken(self._auth_data.refresh_token)
        user_data = self._auth_helpers.parseJWT(self._auth_data.access_token, public_key)
        return user_data

    def getAccessToken(self) -> Optional[str]:
        """
        Get the access token response data.
        :return: Dict containing token data.
        """
        if not self.getUserProfile():
            # We check if we can get the user profile.
            # If we can't get it, that means the access token (JWT) was invalid or expired.
            return None
        return self._auth_data.access_token

    def refreshAccessToken(self) -> None:
        """
        Refresh the access token when it expired.
        """
        self._storeAuthData(self._auth_helpers.getAccessTokenUsingRefreshToken(self._auth_data.refresh_token))
        self.onAuthStateChanged.emit(True)
    
    def deleteAuthData(self):
        """Delete authentication data from preferences and locally."""
        self._storeAuthData()
        self.onAuthStateChanged.emit(False)

    def startAuthorizationFlow(self) -> None:
        """Start a new OAuth2 authorization flow."""
        
        Logger.log("d", "Starting new OAuth2 flow...")
        
        # Create the tokens needed for the code challenge (PKCE) extension for OAuth2.
        # This is needed because the CuraDrivePlugin is a untrusted (open source) client.
        # More details can be found at https://tools.ietf.org/html/rfc7636.
        verification_code = self._auth_helpers.generateVerificationCode()
        challenge_code = self._auth_helpers.generateVerificationCodeChallenge(verification_code)
        
        # Create the query string needed for the OAuth2 flow.
        query_string = urlencode({
            "client_id": OAuth2Settings.CLIENT_ID,
            "redirect_uri": OAuth2Settings.CALLBACK_URL,
            "scope": OAuth2Settings.CLIENT_SCOPES,
            "response_type": "code",
            "state": "CuraDriveIsAwesome",
            "code_challenge": challenge_code,
            "code_challenge_method": "S512"
        })
        
        # Open the authorization page in a new browser window.
        webbrowser.open_new("{}?{}".format(self._OAuth2Settings.AUTH_URL, query_string))
        
        # Start a local web server to receive the callback URL on.
        self._startWebServer(verification_code)

    def _startWebServer(self, verification_code: str) -> None:
        """Start the local web server to handle the authorization callback."""

        Logger.log("d", "Starting local web server to handle authorization callback on port %s", self._web_server_port)
        
        # Create the server and inject the callback and code.
        self._web_server = AuthorizationRequestServer(("0.0.0.0", self._web_server_port), AuthorizationRequestHandler)
        self._web_server.setAuthorizationHelpers(self._auth_helpers)
        self._web_server.setAuthorizationCallback(self._onAuthStateChanged)
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

    def _onAuthStateChanged(self, auth_response: "AuthenticationResponse") -> None:
        """Callback method for a successful authentication flow."""
        if auth_response.success:
            self._storeAuthData(auth_response)
            self.onAuthStateChanged.emit(True)
        else:
            self.onAuthenticationError.emit(False, auth_response.err_message)
        self._stopWebServer()  # Stop the web server at all times.

    def _loadAuthData(self) -> None:
        """Load authentication data from preferences if available."""
        self._cura_preferences.addPreference(self.AUTH_DATA_PREFERENCE_KEY, "{}")  # Ensure the preference exists.
        try:
            preferences_data = json.loads(self._cura_preferences.getValue(self.AUTH_DATA_PREFERENCE_KEY))
            if preferences_data:
                self._auth_data = AuthenticationResponse(**preferences_data)
                self.onAuthStateChanged.emit(True)
        except ValueError as err:
            Logger.log("w", "Could not load auth data from preferences: %s", err)

    def _storeAuthData(self, auth_data: Optional["AuthenticationResponse"] = None) -> None:
        """Store authentication data in preferences and locally."""
        self._auth_data = auth_data
        if auth_data:
            self._user_profile = self.getUserProfile()
            self._cura_preferences.setValue(self.AUTH_DATA_PREFERENCE_KEY, json.dumps(vars(auth_data)))
        else:
            self._user_profile = None
            self._cura_preferences.resetPreference(self.AUTH_DATA_PREFERENCE_KEY)
