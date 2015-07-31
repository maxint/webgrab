# coding: utf-8

import logging
import sys


def setup_logging(name, log_path=None):
    if log_path is None:
        log_path = name + '.log'

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-5.5s - %(message)s')
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    formatter = logging.Formatter('[%(levelname)-1.1s] %(message)s')
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
