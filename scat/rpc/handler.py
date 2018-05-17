# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/3 21:01
"""
import json

from scat.rpc.response import RPCResponseError, RPCResponseSuccess


class RPCHandler:
    def data_received(self, message_data):
        request = self.parse_request(message_data)
        if isinstance(request, RPCResponseError):
            return self.parse_response(request)
        response = self.dispatch(request[0], request[1])
        return self.parse_response(response)

    def dispatch(self, method_name, params):
        method = getattr(self, method_name, None)
        if not method:
            return RPCResponseError(RPCResponseError.method_not_found)

        args = []
        kwargs = {}
        if isinstance(params, dict):
            kwargs = params
        elif type(params) in (list, tuple):
            args = params
        else:
            # Bad argument formatting?
            return RPCResponseError(RPCResponseError.invalid_params)

        try:
            response = method(*args, **kwargs)
        except Exception:
            return RPCResponseError(RPCResponseError.internal_error)

        return response

    def parse_request(self, data):
        try:
            request_data = json.loads(data.decode())
        except Exception:
            return RPCResponseError(RPCResponseError.invalid_params)

        if isinstance(request_data, int) or 'method' not in request_data or 'params' not in request_data:
            return RPCResponseError(RPCResponseError.invalid_params)

        return request_data['method'], request_data['params']

    def parse_response(self, response):
        if isinstance(response, RPCResponseError):
            return json.dumps(response()).encode()
        return json.dumps(RPCResponseSuccess(result=response)()).encode()


if __name__ == '__main__':
    pass
