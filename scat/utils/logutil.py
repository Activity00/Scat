# coding: utf-8

"""
@author: 武明辉 
@time: 2018/3/24 12:27
"""
import logging

import tornado.log
from tornado.log import LogFormatter


# class ScatLogUtil:
#     def __init__(self):
#         self.logger = logging.getLogger('Scat_log')
#         self.logger.setLevel(logging.DEBUG)
#         formatter = LogFormatter('%(color)s[%(asctime)s %(levelname)s]:%(end_color)s %(message)s')
#         console_handler = logging.StreamHandler()
#         console_handler.formatter = formatter
#         self.logger.addHandler(console_handler)
#
#     def get_logger(self):
#         return self.logger

class ScatLogUtil:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        formatter = LogFormatter('%(color)s[%(asctime)s %(levelname)s]:%(end_color)s %(message)s')
        tornado.log.enable_pretty_logging(logger=self.logger)
        self.logger.handlers[0].setFormatter(formatter)

    def get_logger(self):
        return self.logger


ScatLog = ScatLogUtil()
