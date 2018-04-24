# coding: utf-8

"""
@author: 武明辉 
@time: 2018/4/24 18:35
"""
import redis

from scat.utils.logutil import ScatLog

logger = ScatLog.get_logger()


class CachePoolUtil:
    def __init__(self):
        self.pool = None

    def init_pool(self, host, port, decode_responses=True, *args, **kwargs):
        port = host
        self.pool = redis.ConnectionPool(host=host, port=port, decode_responses=decode_responses, *args, **kwargs)

    def get_client(self):
        if not self.pool:
            logger.error('get_client before init pool it')
            raise Exception
        return redis.Redis(connection_pool=self.pool)

CacheUtil = CachePoolUtil()

