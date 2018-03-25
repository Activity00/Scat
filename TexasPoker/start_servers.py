# coding: utf-8

"""
@author: 武明辉 
@time: 2018/3/23 17:22
"""
import os

if __name__ == '__main__':
    os.environ.setdefault("SCAT_SETTINGS_MODULE", "TexasPoker.settings")
    from scat.distributed.master import Master
    master = Master()
    master.start('', 1)
