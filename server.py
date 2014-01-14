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
import uuid
from ol_const import static
import json
import datetime
from http import cookies

logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('ol')

tree = ElementTree.parse("server.xml").findall('mime-mapping')
mime_mappings = {}
logger.debug('load server.xml')
for child in tree:
    mime_mappings[child.attrib['extension']] = child.attrib['mime-type']

hostIP = '192.168.1.130'
portNum = 8081

# if platform.system() == 'Windows':
#     output = os.popen('netstat -aon|findstr ":"' + str(portNum)).readlines()
#     for i in output:
#         os.popen('taskkill /f /pid ' + re.split('\s+', i.strip())[4])
#         pass

assets = 'page'


class SessionScope():
    sessions = {}

    def createSession(self):
        sessionId = str(uuid.uuid4())
        self.sessions[sessionId] = {'createTime': datetime.datetime.now()}
        print(self.sessions)
        return sessionId

    def getSession(self, sessionId):
        return self.sessions[sessionId]

sessionScope = SessionScope()
sessionScope.createSession()


class OpticalineServer(BaseHTTPRequestHandler):

    def do_head(self):
        self.analysis(static.method.HEAD)

    def do_GET(self):
        #print(self.headers.items())
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
            cookie = self.headers.get('Cookie') or ""
            if len(cookie) > 0:
                cookie = {a.split("=")[0]:a.split("=")[1] for a in cookie.split(";")}
            else:
                cookie = {}

            if not cookie.get('SESSIONID') :
                cookie['SESSIONID'] = sessionScope.createSession()
                #JSESSIONID=86D6E5C39785133684568CDE3A9984EC; Path=/ylbl/; HttpOnly
                self.send_header("Set-Cookie", "SESSIONID=" + cookie['SESSIONID'] + "; Path=/; HttpOnly")
            session = sessionScope.getSession(cookie['SESSIONID'])
            print(session)
            response = self.request_dynamic(method)
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def request_dynamic(self, method):
        logger.debug('same connect do method - %s' % method)
        self.send_response(200, message=None)
        request = urlparse(self.path)
        if method == static.method.GET:
            params = urllib.parse.unquote(request.query)
        else:
            length = int(self.headers['Content-Length'])
            params = self.rfile.read(length).decode('utf-8')
        params = self.__param_easy_2_use(params)
        # TODO 调用 controller处理对应请求
        extension = os.path.splitext(request.path)[1]
        if extension == '':
            extension = '*'
        print(os.path.splitext(request.path)[0])
        self.send_header('Content-type', mime_mappings[extension])
        return '{"name":"lilei2"}'.encode(encoding='utf_8', errors='strict')

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
        params = urllib.parse.parse_qs(params)
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
