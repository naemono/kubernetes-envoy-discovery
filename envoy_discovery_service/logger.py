import logging

from pythonjsonlogger import jsonlogger


def setup_logging():
    """Setup logging configuration"""
    format_str = '%(message)%(levelname)%(name)%(asctime)'
    logger = logging.getLogger('')
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(format_str)
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel('INFO')
    logger.propagate = False
    return
