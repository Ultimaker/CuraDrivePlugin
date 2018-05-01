# Copyright (c) 2017 Ultimaker B.V.
from http.server import HTTPServer


class AuthorizationRequestServer(HTTPServer):

    def setAuthorizationCallback(self, authorization_callback) -> None:
        self.RequestHandlerClass.authorization_callback = authorization_callback

    def setCodeVerifier(self, code_verifier: str) -> None:
        self.RequestHandlerClass.code_verifier = code_verifier
