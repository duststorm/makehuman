#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Logging.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Logging component. To be used instead of print statements.
"""

import sys
import os
import logging
import logging.config
import code
from logging import debug, warning, error, getLogger

from core import G
from getpath import getPath

NOTICE = 25
MESSAGE = logging.INFO

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

logging.addLevelName(NOTICE, "NOTICE")
logging.addLevelName(MESSAGE, "MESSAGE")

def _splitpath(path):
    
    head, tail = os.path.split(path)
    if tail == '':
        return [head]
    return _splitpath(head) + [tail]

class NoiseFilter(logging.Filter):
    def filter(self, record):
        try:
            if record.msg.endswith(':\n%s'):
                record.msg = record.msg[:-4]
                record.args = record.args[:-1]
        except:
            import traceback
            traceback.print_exc()
        return True

class SplashLogHandler(logging.Handler):
    def emit(self, record):
        if G.app is not None and G.app.splash is not None:
            G.app.splash.logMessage(self.format(record).split('\n',1)[0] + '\n')

class StatusLogHandler(logging.Handler):
    def emit(self, record):
        if G.app is not None and G.app.statusBar is not None:
            G.app.statusBar.showMessage("%s", self.format(record))

class ApplicationLogHandler(logging.Handler):
    def emit(self, record):
        if G.app is not None and G.app.log_window is not None:
            G.app.log_window.addText(self.format(record) + '\n')

_logger_notice_src = r'''
def _logger_notice(self, msg, *args, **kwargs):
    self.log(NOTICE, msg, *args, **kwargs)
'''
try:
    exec(code.compile_command(_logger_notice_src, logging.info.func_code.co_filename))
except:
    def _logger_notice(self, format, *args, **kwargs):
        self.log(NOTICE, format, *args, **kwargs)

class Logger(logging.Logger):
    message = logging.Logger.info
    notice = _logger_notice

def init():
    def config():
        userDir = getPath('')
        defaults = dict(mhUserDir = userDir.replace('\\','/'))

        try:
            filename = os.path.join(userDir, "logging.ini")
            if os.path.isfile(filename):
                logging.config.fileConfig(filename, defaults)
                return
        except Exception:
            pass

        try:
            logging.config.fileConfig(os.path.join('data','logging.ini'), defaults)
            return
        except Exception:
            pass

        try:
            logging.basicConfig(level = logging.DEBUG)
            return
        except Exception:
            pass

    logging.setLoggerClass(Logger)

    logging.getLogger('mh.callAsync').setLevel(logging.WARNING)
    logging.getLogger('mh.callEvent').setLevel(logging.WARNING)

    config()

    logging.captureWarnings(True)

    try:
        logging.getLogger('OpenGL.formathandler').addFilter(NoiseFilter())
    except Exception:
        import traceback
        traceback.print_exc()
