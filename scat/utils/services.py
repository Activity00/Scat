# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/21 14:04
"""


class Service:
    def __init__(self, name, app):
        self.name = name
        self.app = app
        self._target = {}

    def get_target(self, target_key):
        return self._target.get(target_key, None)

    def call_target(self, target_key, *args, **kwargs):
        target = self.get_target(target_key)
        if not target_key:
            print('no target')
            return None

        return target(*args, **kwargs)

    def map_target(self):
        pass

    def unmap_target(self):
        pass

