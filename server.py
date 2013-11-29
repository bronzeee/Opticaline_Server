# encoding=utf-8
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse
from xml.etree import ElementTree
import os
import platform
import re

tree = ElementTree.parse("server.xml").findall('mime-mapping')
mime_mappings = {}
for child in tree:
    mime_mappings[child.attrib['extension']] = child.attrib['mime-type']

hostIP = 'localhost'
portNum = 8080

if platform.system() == 'Windows':
    output = os.popen('netstat -aon|findstr ":"' + str(portNum)).readlines()
    for i in output:
        os.popen('taskkill /f /pid ' + re.split('\s+', i.strip())[4])

assets = 'page'


class OpticalineServer(BaseHTTPRequestHandler):

    def do_head(self):
        pass

    def do_GET(self):
        try:
            result = urlparse(self.path)
            self.send_response(200, message=None)
            if result.path == '/':
                file_path = assets + 'index.html'
            else:
                file_path = assets + result.path
            if result.path.endswith('.html'):
                self.send_header('Content-type', mime_mappings['html'])
                self.end_headers()
                response = open(file_path, 'r').read().encode(
                    encoding='utf_8', errors='strict')
            else:
                self.send_header('Content-type', mime_mappings['pdf'])
                self.end_headers()
                response = open(file_path, 'rb').read()
            self.wfile.write(response)
        except IOError:
            self.send_error(404, message=None)

    def do_POST(self):
        pass


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

print("start server with %d port" % portNum)
myServer = ThreadingHttpServer((hostIP, portNum), OpticalineServer)
myServer.serve_forever()
myServer.server_close()
