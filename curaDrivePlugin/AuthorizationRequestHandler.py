# Copyright (c) 2017 Ultimaker B.V.
import json

import os.path
from collections import namedtuple
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlencode

import requests

from curaDrivePlugin.Settings import Settings

ResponseStatus = namedtuple("HTTPStatus", ["code", "message"])

ResponseData = namedtuple("ResponseData", ["status", "content_type", "data_stream"])

HTTP_STATUS = {
    "OK": ResponseStatus(code=200, message="OK"),
    "NOT_FOUND": ResponseStatus(code=404, message="NOT FOUND")
}


class AuthorizationRequestHandler(BaseHTTPRequestHandler):

    TOKEN_URL = "{}/token".format(Settings.OAUTH_SERVER_URL)

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.authorization_callback = None
        self.code_verifier = None
        self._token_response = None

    def do_GET(self):
        """Entry point for GET requests"""

        # Extract values from the query string.
        path, _, query_string = self.path.partition('?')
        query = parse_qs(query_string)

        # Handle the possible requests
        if path == "/callback":
            response = self._routeCallback(path, query)
        else:
            response = self._routeNotFound(path, query)

        self._sendHeaders(response.status, response.content_type)
        self._sendData(response.data_stream)

        if self._token_response:
            # Trigger the callback if we got a response.
            # This will cause the server to shut down, so we do it at the very end of the request handling.
            self.authorization_callback(self._token_response)
            self._token_response = None

        return True

    def _requestAccessToken(self, authorization_code: str, code_verifier: str) -> dict:
        r = requests.post(self.TOKEN_URL, data={
            "client_id": Settings.CLIENT_ID,
            "redirect_uri": Settings.CALLBACK_URL,
            "grant_type": "authorization_code",
            "code": authorization_code,
            "code_verifier": code_verifier
        })
        return json.loads(r.text)

    def _routeCallback(self, path: str, query: dict) -> "ResponseData":
        authorization_code = self._queryGet(query, "code")
        authorization_state = self._queryGet(query, "state")
        self._token_response = self._requestAccessToken(authorization_code, self.code_verifier)
        self._token_response["state"] = authorization_state
        html_stream = open(os.path.join(os.path.dirname(__file__), "html", "callback.html"), "rb")
        data = html_stream.read()
        html_stream.close()
        return ResponseData(status=HTTP_STATUS["OK"], content_type="text_html", data_stream=data)

    def _routeNotFound(self, path: str, query: dict) -> "ResponseData":
        return ResponseData(status=HTTP_STATUS["NOT_FOUND"], content_type="text_html", data_stream="")

    def _sendHeaders(self, status, content_type) -> None:
        """Send out the headers"""
        self.send_response(status.code, status.message)
        self.send_header('Content-type', content_type)
        self.send_header('Transfer-Encoding', 'chunked')
        self.send_header('Connection', 'close')
        self.end_headers()

    def _sendData(self, data) -> None:
        """Send out the data"""
        self.wfile.write(data)

    @staticmethod
    def _queryGet(query_data: dict, key: str, default="") -> str:
        """Helper for getting values from a pre-parsed query string"""
        return query_data.get(key, [default])[0]
