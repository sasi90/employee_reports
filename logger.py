import logging
from logging.handlers import TimedRotatingFileHandler
# from logging.handlers import RotatingFileHandler
import os

formatter = logging.Formatter('%(levelname)s | %(asctime)s | module: %(module)s | lineno: %(lineno)d | %(message)s')


# def setup_logger(name, log_file, level=logging.INFO):
#     """To setup as many loggers as you want"""
#
#     handler = logging.FileHandler(log_file)
#     handler.setFormatter(formatter)
#
#     logger = logging.getLogger(name)
#     logger.setLevel(level)
#     logger.addHandler(handler)
#
#     return logger
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = TimedRotatingFileHandler(log_file, when='midnight')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

Trace_file_path = 'logs/traces.log'
Exe_file_path = 'logs/exceptions.log'

if not os.path.exists(Trace_file_path):
    open(Trace_file_path, 'w+')

if not os.path.exists(Exe_file_path):
    open(Exe_file_path, 'w+')


trace = setup_logger('first_logger', 'logs/traces.log')
exc = setup_logger('second_logger', 'logs/exceptions.log')
