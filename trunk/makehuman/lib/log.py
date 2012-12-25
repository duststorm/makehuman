
import sys
import os
import logging
import logging.config
import code
from logging import debug, warning, error

from core import G
from getpath import getPath

NOTICE = 25

message = logging.info

# We have to make notice() appear to have been defined in the logging module
# so that logging.findCaller() finds its caller, not notice() itself
# This is required for the pathname, filename, module, funcName and lineno
# members of the LogRecord refer to the caller rather than to notice() itself.

_notice_src = r'''
def notice(format, *args, **kwargs):
    logging.info(format, *args, **kwargs)
'''
try:
    exec(code.compile_command(_notice_src, logging.info.func_code.co_filename))
except:
    def notice(format, *args, **kwargs):
        logging.log(NOTICE, format, *args, **kwargs)

logging.addLevelName(NOTICE, "notice")

class SplashLogHandler(logging.Handler):
    def emit(self, record):
        if G.app is not None and G.app.splash is not None:
            G.app.splash.logMessage(self.format(record).split('\n',1)[0] + '\n')

class ApplicationLogHandler(logging.Handler):
    def emit(self, record):
        if G.app is not None and G.app.log_window is not None:
            G.app.log_window.addText(self.format(record) + '\n')

defaultConfig = {
    'version': 1,
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'stream': sys.stdout
            },
        'splash': {
            'class': 'log.SplashLogHandler',
            'level': logging.DEBUG
            },
        'app': {
            'class': 'log.ApplicationLogHandler',
            'level': logging.DEBUG
            }
        },
    'root': {
        'level': logging.DEBUG,
        'handlers': ['stdout', 'splash', 'app']
        }
    }

try:
    _filename = os.path.join(getPath(''), "makehuman.log")
    with open(_filename, 'w') as f:
        pass
    defaultConfig['handlers']['file'] = {
        'class': 'logging.FileHandler',
        'level': logging.DEBUG,
        'filename': _filename
        }
    defaultConfig['root']['handlers'].append('file')
except:
    pass

def init():
    logging.config.dictConfig(defaultConfig)
    filename = os.path.join(getPath(''), "logging.ini")
    if os.path.isfile(filename):
        logging.config.fileConfig(filename)
