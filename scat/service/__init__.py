# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/21 14:04

master_service
web_service
ws_service
RemoteService
"""
from twisted.internet import defer, threads
from twisted.python import log
import tornado.web
import tornado.websocket
import threading
from scat import ScatObject


def master_service(target):
    ScatObject.master_remote.get_service().map_target(target)


def root_service(target):
    ScatObject.root.service.map_target(target)


def web_service(cls):
    if ScatObject.web_root:
        url = getattr(cls, 'URL', None)
        base = cls.__base__ if tornado.web.RequestHandler in cls.__base__.mro() else None
        handler_cls = type(cls.__name__, (base or tornado.web.RequestHandler,), dict(cls.__dict__))
        ScatObject.web_root.add_handlers(r'.*$', [(url or r'/{}/'.format(handler_cls.__name__.lower()), handler_cls), ])


def ws_service(cls):
    if ScatObject.web_root:
        url = getattr(cls, 'URL', None)
        base = cls.__base__ if tornado.websocket.WebSocketHandler in cls.__base__.mro() else None
        handler_cls = type(cls.__name__, (base or tornado.websocket.WebSocketHandler,), dict(cls.__dict__))
        ScatObject.web_root.add_handlers(r'.*$', [(url or r'/{}/'.format(handler_cls.__name__.lower()), handler_cls), ])


class RemoteService:
    def __init__(self, remote_name):
        self.remote_name = remote_name

    def __call__(self, target):
        ScatObject.remote[self.remote_name].get_service().map_target(target)


class Service:
    SINGLE_STYLE = 1
    PARALLEL_STYLE = 2

    def __init__(self, name, run_style=SINGLE_STYLE):
        self.name = name
        self._run_style = run_style
        self._targets = {}
        self._lock = threading.RLock()

    def get_target(self, target_key):
        """Get a target from the service by name."""
        self._lock.acquire()
        try:
            target = self._targets.get(target_key, None)
        finally:
            self._lock.release()
        return target

    def map_target(self, target):
        """Add a target to the service."""
        key = target.__name__
        if key in self._targets:
            exist_target = self._targets.get(key)
            raise "target [%d] Already exists,\
            Conflict between the %s and %s" % (key, exist_target.__name__, target.__name__)
        self._targets[key] = target

    def un_map_target(self, target):
        """Remove a target from the service."""
        self._lock.acquire()
        try:
            key = target.__name__
            if key in self._targets:
                del self._targets[key]
        finally:
            self._lock.release()

    def un_map_target_by_key(self, target_key):
        """Remove a target from the service."""
        self._lock.acquire()
        try:
            del self._targets[target_key]
        finally:
            self._lock.release()

    def call_target(self, target_key, *args, **kwargs):
        if self._run_style == self.SINGLE_STYLE:
            result = self.call_target_single(target_key, *args, **kwargs)
        else:
            result = self.call_target_parallel(target_key, *args, **kwargs)
        return result

    def call_target_single(self, target_key, *args, **kwargs):
        target = self.get_target(target_key)

        self._lock.acquire()
        try:
            if not target:
                log.err('the command ' + str(target_key) + ' not Found on service')
                return None

            defer_data = target(*args, **kwargs)
            if not defer_data:
                return None
            if isinstance(defer_data, defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d

    def call_target_parallel(self, target_key, *args, **kw):

        self._lock.acquire()
        try:
            target = self.get_target(target_key)
            if not target:
                log.err('the command ' + str(target_key) + ' not Found on service')
                return None
            log.msg("call method %s on service[parallel]" % target.__name__)
            d = threads.deferToThread(target, *args, **kw)
        finally:
            self._lock.release()
        return d

