# Copyright (c) 2017 Ultimaker B.V.
import os.path
import json
from typing import Optional, Callable

import requests

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from UM.Logger import Logger
from curaDrivePlugin.Settings import Settings
from curaDrivePlugin.authorization.AuthorizationHelpers import AuthenticationResponse, ResponseData, HTTP_STATUS, \
    ResponseStatus


class AuthorizationRequestHandler(BaseHTTPRequestHandler):
    """
    This handler handles all HTTP requests on the local web server.
    It also requests the access token for the 2nd stage of the OAuth flow.
    """

    TOKEN_URL = "{}/token".format(Settings.OAUTH_SERVER_URL)
    
    OAUTH_GRANT_TYPE = "authorization_code"

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        
        # These values will be injected by the HTTPServer that this handler belongs to.
        self.authorization_callback = None  # type: Callable[[AuthenticationResponse], None]
        self.verification_code = None  # type: str

    def do_GET(self):
        """Entry point for GET requests"""

        # Extract values from the query string.
        path, _, query_string = self.path.partition('?')
        query = parse_qs(query_string)
        token_response = None

        # Handle the possible requests
        if path == "/callback":
            server_response, token_response = self._handleCallback(query)
        else:
            server_response = self._handleNotFound()

        # Send the data to the browser.
        self._sendHeaders(server_response.status, server_response.content_type)
        self._sendData(server_response.data_stream)

        if token_response:
            # Trigger the callback if we got a response.
            # This will cause the server to shut down, so we do it at the very end of the request handling.
            self.authorization_callback(token_response)

    def _requestAccessToken(self, authorization_code: str) -> Optional["AuthenticationResponse"]:
        """
        Request the access token from the authorization server.
        :param authorization_code: The authorization code from the 1st step.
        :return: A dict containing the access token and some other data.
        """
        token_request = requests.post(self.TOKEN_URL, data={
            "client_id": Settings.CLIENT_ID,
            "redirect_uri": Settings.CALLBACK_URL,
            "grant_type": self.OAUTH_GRANT_TYPE,
            "code": authorization_code,
            "code_verifier": self.verification_code
        })
        token_data = None
        
        try:
            token_data = json.loads(token_request.text)
        except ValueError as err:
            Logger.log("w", "Could not parse token response data: %s", err)
        
        if not token_data:
            return AuthenticationResponse(success = False, err_message = "Could not read response.")
        
        if token_request.status_code != 200:
            return AuthenticationResponse(success = False, err_message = token_data["error_description"])
            
        return AuthenticationResponse(success = True,
                                      token_type = token_data["token_type"],
                                      access_token = token_data["access_token"],
                                      refresh_token = token_data["refresh_token"],
                                      expires_in = token_data["expires_in"],
                                      scope = token_data["scope"])

    def _handleCallback(self, query: dict) -> ("ResponseData", Optional["AuthenticationResponse"]):
        """
        Handler for the callback URL redirect.
        :param query: Dict containing the HTTP query parameters.
        :return: HTTP ResponseData containing a success page to show to the user.
        """
        token_response = self._requestAccessToken(self._queryGet(query, "code"))
        with open(os.path.join(os.path.dirname(__file__), "html", "callback.html"), "rb") as data:
            return ResponseData(status = HTTP_STATUS["OK"], content_type = "text_html", data_stream = data.read()),\
                   token_response

    @staticmethod
    def _handleNotFound() -> "ResponseData":
        """Handle all other non-existing server calls."""
        return ResponseData(status=HTTP_STATUS["NOT_FOUND"], content_type="text/html", data_stream="")

    def _sendHeaders(self, status: "ResponseStatus", content_type) -> None:
        """Send out the headers"""
        self.send_response(status.code, status.message)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _sendData(self, data: bytes) -> None:
        """Send out the data"""
        self.wfile.write(data)

    @staticmethod
    def _queryGet(query_data: dict, key: str, default="") -> str:
        """Helper for getting values from a pre-parsed query string"""
        return query_data.get(key, [default])[0]
