# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/4 14:34
"""
from scat.server.globalobject import GlobalObject
from scat.utils.services import Service

net_service = Service("loginService", None)


def net_service_handle(target):
    net_service.map_target(target)


GlobalObject().net_app.add_service_channel(net_service)
