# coding: utf-8

"""
@author: 武明辉 
@time: 2018/3/24 12:27
"""
import logging
from logging.handlers import TimedRotatingFileHandler

import tornado.log
from tornado.log import LogFormatter


FORMATTER = LogFormatter('%(color)s[%(asctime)s %(levelname)s]:%(end_color)s %(message)s')


class ScatLogUtil:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        tornado.log.enable_pretty_logging(logger=self.logger)
        self.logger.handlers[0].setFormatter(FORMATTER)

    def get_logger(self):
        return self.logger


def set_file_handler(log_path):
    fh = TimedRotatingFileHandler(log_path, when='M', interval=1, backupCount=30)
    fh.setFormatter(FORMATTER)
    logging.getLogger().addHandler(fh)


ScatLog = ScatLogUtil()
