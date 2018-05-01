# Copyright (c) 2017 Ultimaker B.V.
import http.server
import socketserver

from UM.Logger import Logger


class WebServer:

    PORT = 1337

    def __init__(self):
        self._handler = None  # type: http.server.SimpleHTTPRequestHandler

    def run(self):
        self._handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.PORT), self._handler) as httpd:
            Logger.log("i", "Running local web server to handle authorization callback on port %s", self.PORT)
            httpd.serve_forever()
