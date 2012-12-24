
import logging
from logging import debug, warning, error

NOTICE = 25

def message(format, *args, **kwargs):
    logging.info(format, *args, **kwargs)

def notice(format, *args, **kwargs):
    logging.log(NOTICE, format, *args, **kwargs)

logging.addLevelName(NOTICE, "notice")
