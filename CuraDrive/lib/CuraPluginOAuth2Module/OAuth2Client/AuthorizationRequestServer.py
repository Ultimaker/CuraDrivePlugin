# Copyright (c) 2017 Ultimaker B.V.
from http.server import HTTPServer

from .AuthorizationHelpers import AuthorizationHelpers


class AuthorizationRequestServer(HTTPServer):
    """
    The authorization request callback handler server.
    This subclass is needed to be able to pass some data to the request handler.
    This cannot be done on the request handler directly as the HTTPServer creates an instance of the handler after init.
    """

    def setAuthorizationHelpers(self, authorization_helpers: "AuthorizationHelpers") -> None:
        """Set the authorization helpers instance on the request handler."""
        self.RequestHandlerClass.authorization_helpers = authorization_helpers

    def setAuthorizationCallback(self, authorization_callback) -> None:
        """Set the authorization callback on the request handler."""
        self.RequestHandlerClass.authorization_callback = authorization_callback

    def setVerificationCode(self, verification_code: str) -> None:
        """Set the verification code on the request handler."""
        self.RequestHandlerClass.verification_code = verification_code
