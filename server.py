# encoding=utf-8
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse
import urllib
from xml.etree import ElementTree
import os
import platform
import re
import logging
import logging.config
from ol_const import static
import json

logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('ol')

tree = ElementTree.parse("server.xml").findall('mime-mapping')
mime_mappings = {}
logger.debug('load server.xml')
for child in tree:
    mime_mappings[child.attrib['extension']] = child.attrib['mime-type']

hostIP = 'localhost'
portNum = 8080

# if platform.system() == 'Windows':
#     output = os.popen('netstat -aon|findstr ":"' + str(portNum)).readlines()
#     for i in output:
# os.popen('taskkill /f /pid ' + re.split('\s+', i.strip())[4])
#         pass

assets = 'page'


class OpticalineServer(BaseHTTPRequestHandler):

    def do_head(self):
        analysis(static.method.HEAD)

    def do_GET(self):
        self.analysis(static.method.GET)

    def do_POST(self):
        self.analysis(static.method.POST)

    def do_PUT(self):
        self.analysis(static.method.PUT)

    def analysis(self, method):
        request = urlparse(self.path)
        if(os.path.isfile(assets + request.path)):
            response = self.request_file(assets + request.path)
        else:
            response = self.request_dynamic(method)
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def request_dynamic(self, method):
        logger.debug('same connect do method - %s' % method)
        self.send_response(200, message=None)
        self.send_header('Content-type', 'text/json')
        request = urlparse(self.path)
        if method == static.method.GET:
            params = urllib.parse.parse_qs(urllib.parse.unquote(request.query))
        else:
            length = int(self.headers['Content-Length'])
            params = urllib.parse.parse_qs(
                self.rfile.read(length).decode('utf-8'))

        params = self.__param_easy_2_use(params)

        # TODO 调用 controller处理对应请求
        return '{"name":"lilei"}'.encode(encoding='utf_8', errors='strict')

    def request_file(self, filePath):
        try:
            self.send_response(200, message=None)
            extension = os.path.splitext(filePath)[1]
            if extension == '':
                extension = '*'
            self.send_header('Content-type', mime_mappings[extension])
            return open(filePath, 'rb').read()
        except IOError:
            self.send_error(404, message=None)

    def __param_easy_2_use(self, params):
        for key in params.keys():
            if len(params[key]) == 1:
                params[key] = params[key][0]
        return params


class ThreadingHttpServer(ThreadingMixIn, HTTPServer):
    pass

print("start server with %d port" % portNum)
myServer = ThreadingHttpServer((hostIP, portNum), OpticalineServer)
myServer.serve_forever()
myServer.server_close()
