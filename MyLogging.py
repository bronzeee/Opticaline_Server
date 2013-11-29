import logging
import logging.config

logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('simpleExample')

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')


# http://stackoverflow.com/questions/18157527/python-via-tor-connectionrefusederror-winerror-10061

# http://docs.python.org/3.3/library/logging.config.html
