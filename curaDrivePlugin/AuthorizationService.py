# Copyright (c) 2017 Ultimaker B.V.
from curaDrivePlugin.WebServer import WebServer


class AuthorizationService:
    """
    The authorization service is responsible for handling the login flow,
    storing user credentials and providing account information.
    """

    def __init__(self):
        self._web_server = WebServer()

    def getUserProfile(self):
        pass

    def startAuthorizationFlow(self):
        self._web_server.run()
