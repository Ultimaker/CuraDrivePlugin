# Copyright (c) 2017 Ultimaker B.V.
import http.server
import socketserver

from UM.Logger import Logger


class WebServer:

    PORT = 1337

    def __init__(self):
        self._handler = http.server.SimpleHTTPRequestHandler

    def run(self):
        Logger.log("i", "Starting local web server to handle authorization callback on port %s", self.PORT)
        with socketserver.TCPServer(("0.0.0.0", self.PORT), self._handler) as httpd:
            httpd.serve_forever()
