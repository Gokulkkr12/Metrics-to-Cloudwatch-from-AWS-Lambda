"""Lambda Logging with python-json-logger module"""
import logging
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
FORMAT_STR = '%(levelname)%(message)%'
formatter = jsonlogger.JsonFormatter(FORMAT_STR)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False
