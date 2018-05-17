# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/27 12:38
"""
import json


class RPCResponse:
    def __init__(self, code, message, result):
        self.data = {'code': code, 'message': message}
        if result:
            self.data['result'] = result

    def __call__(self):
        return json.dumps(self.data)


class RPCResponseError(RPCResponse):
    parse_error = 'parse_error'
    method_not_found = 'method_not_found'
    invalid_request = 'invalid_request'
    invalid_params = 'invalid_params'
    internal_error = 'internal_error'
    msg_code = {
        'parse_error': -32700,
        'method_not_found': -32601,
        'invalid_request': -32600,
        'invalid_params': -32602,
        'internal_error': -32603
    }

    def __init__(self, message, result=None):
        code = RPCResponseError.msg_code.get(message, -1)
        super(RPCResponseError, self).__init__(code, message, result)


class RPCResponseSuccess(RPCResponse):
    def __init__(self, result=None):
        super(RPCResponseSuccess, self).__init__(0, 'OK', result)
