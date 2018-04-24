# coding: utf-8

"""
@author: 武明辉 
@time: 2018/4/24 18:28
"""


class DBPoolUtil(object):

    def init_pool(self, **kw):
        self.config = kw
        # creator = DBCS.get(kw.get('engine', 'mysql'), MySQLdb)
        # self.pool = PooledDB(creator, 5, **kw)

    def connection(self):
        return self.pool.connection()

DBPool = DBPoolUtil()

