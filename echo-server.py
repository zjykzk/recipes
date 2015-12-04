# -*- coding: utf-8 -*-
# Author : zenk
# 2015-12-04 14:58
#!/usr/bin/python

"""
Save this file as echo-server.py
>>> python echo-server.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python echo-server.py
Serving on localhost:8000

You can use this to test GET and POST methods.

"""
try:
    from http.server import SimpleHTTPRequestHandler, HTTPServer
except ImportError:
    from BaseHTTPServer import SimpleHTTPRequestHandler, HTTPServer 

import logging
import sys


if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""


class ServerHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        self.b.wfile.write("OK")

    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        logging.warning("======= POST VALUES =======")
        data = self.rfile.read(int(self.headers['Content-Length']))
        logging.warning(data)
        logging.warning("\n")
        self.wfile.write(data)
        self.wfile.flush()

Handler = ServerHandler

httpd = HTTPServer(("", PORT), Handler)

print("@zhangkai Python http server version 0.1 (for testing purposes only)")
print("Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT))
httpd.serve_forever()
