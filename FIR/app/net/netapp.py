# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/4 14:17
"""
from FIR.app.net.service import net_service_handle
from scat import ScatObject


@net_service_handle
def forward(command, data):
    ScatObject.remote['gate'].fowarding(command, data)
