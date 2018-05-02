# Copyright (c) 2017 Ultimaker B.V.
import os.path
from typing import Optional, Callable

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from curaDrivePlugin.authorization.AuthorizationHelpers import AuthorizationHelpers
from curaDrivePlugin.authorization.models import AuthenticationResponse, ResponseData, HTTP_STATUS, ResponseStatus


class AuthorizationRequestHandler(BaseHTTPRequestHandler):
    """
    This handler handles all HTTP requests on the local web server.
    It also requests the access token for the 2nd stage of the OAuth flow.
    """

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

    def _handleCallback(self, query: dict) -> ("ResponseData", Optional["AuthenticationResponse"]):
        """
        Handler for the callback URL redirect.
        :param query: Dict containing the HTTP query parameters.
        :return: HTTP ResponseData containing a success page to show to the user.
        """
        token_response = AuthorizationHelpers.getAccessTokenUsingAuthorizationCode(self._queryGet(query, "code"),
                                                                                   self.verification_code)
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
