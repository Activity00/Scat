# coding: utf-8

"""
@author: 武明辉 
@time: 2018/3/24 12:27
"""
from twisted.python.log import ILogObserver


class ScatLog(ILogObserver):

    def __init__(self, log_path):
        self.file = open(log_path, 'w')

    def __call__(self, eventDict):
        if 'logLevel' in eventDict:
            level = eventDict['logLevel']
        elif eventDict['isError']:
            level = 'ERROR'
        else:
            level = 'INFO'
        text = log.textFromEventDict(eventDict)
        if text is None or level != 'ERROR':
            return
        nowdate = datetime.datetime.now()
        self.file.write('[' + str(nowdate) + ']\n' + str(level) + '\n\t' + text + '\r\n')
        self.file.flush()
