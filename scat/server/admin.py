from importlib import reload

from tornado import ioloop

from scat import ScatObject
from scat.service import master_service
from scat.utils.logutil import ScatLog


logger = ScatLog.get_logger()


@master_service
def server_stop():
    logger.info('stop')
    if ScatObject.stop_handler:
        ScatObject.stop_handler()
    ioloop.IOLoop.current().call_later(0.5, ioloop.IOLoop.current().stop())
    return True


@master_service
def server_reload():
    logger.info('reload')
    if ScatObject.reload_module:
        reload(ScatObject.reload_module)
    return True


@master_service
def remote_connect(remote_name, remote_host):
    ScatObject.remote_connect(remote_name, remote_host)

