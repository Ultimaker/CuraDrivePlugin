# Copyright (c) 2017 Ultimaker B.V.
import os.path
import json
import requests

from collections import namedtuple
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from curaDrivePlugin.Settings import Settings


# Response status template.
ResponseStatus = namedtuple("HTTPStatus", ["code", "message"])

# Response data template.
ResponseData = namedtuple("ResponseData", ["status", "content_type", "data_stream"])

# Possible HTTP responses.
HTTP_STATUS = {
    "OK": ResponseStatus(code=200, message="OK"),
    "NOT_FOUND": ResponseStatus(code=404, message="NOT FOUND")
}


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
        self.authorization_callback = None
        self.verification_code = None
        
        # The token response will be stored temporarily so we can finish the response before stopping the server.
        self._token_response = None

    def do_GET(self):
        """Entry point for GET requests"""

        # Extract values from the query string.
        path, _, query_string = self.path.partition('?')
        query = parse_qs(query_string)

        # Handle the possible requests
        if path == "/callback":
            response = self._handleCallback(query)
        else:
            response = self._handleNotFound()

        # Send the data to the browser.
        self._sendHeaders(response.status, response.content_type)
        self._sendData(response.data_stream)

        if self._token_response:
            # Trigger the callback if we got a response.
            # This will cause the server to shut down, so we do it at the very end of the request handling.
            self.authorization_callback(self._token_response)
            self._token_response = None

    def _requestAccessToken(self, authorization_code: str) -> dict:
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
        return json.loads(token_request.text)

    def _handleCallback(self, query: dict) -> "ResponseData":
        """
        Handler for the callback URL redirect.
        :param query: Dict containing the HTTP query parameters.
        :return: HTTP ResponseData containing a success page to show to the user.
        """
        self._token_response = self._requestAccessToken(self._queryGet(query, "code"))
        with open(os.path.join(os.path.dirname(__file__), "html", "callback.html"), "rb") as data:
            return ResponseData(status = HTTP_STATUS["OK"], content_type = "text_html", data_stream = data)

    @staticmethod
    def _handleNotFound() -> "ResponseData":
        """Handle all other non-existing server calls."""
        return ResponseData(status=HTTP_STATUS["NOT_FOUND"], content_type="text_html", data_stream="")

    def _sendHeaders(self, status, content_type) -> None:
        """Send out the headers"""
        self.send_response(status.code, status.message)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _sendData(self, data) -> None:
        """Send out the data"""
        self.wfile.write(data)

    @staticmethod
    def _queryGet(query_data: dict, key: str, default="") -> str:
        """Helper for getting values from a pre-parsed query string"""
        return query_data.get(key, [default])[0]
