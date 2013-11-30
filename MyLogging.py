import logging
import logging.config

logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('ol')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')


# http://stackoverflow.com/questions/18157527/python-via-tor-connectionrefusederror-winerror-10061

# http://docs.python.org/3.3/library/logging.config.html
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