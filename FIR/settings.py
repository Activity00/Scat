# coding: utf-8


MASTER = {
    "root_host": "localhost",
    "root_port": 9999,
    "web_port": 9998
}

SERVERS = {
    # 'gate': {
    #   'rootport': 10000,
    #   'name': "gate",
    #   'db': True,
    #   'mem': True,
    #   'app': "app.gateserver",
    #   'log': "app/logs/gate.log"
    # },
    'net': {
       'net_port': 10000,
       'net_protocol': 'tcp',    # tcp websocket, socketio
       'name': 'net',
       'remote_list': [
            {
                "root_port": 20001,
                "root_name": "gate"
            }
        ],
       'app': 'app.net_server'
    }
}


DB = {
    "host": "localhost",
    "user": "root",
    "passwd": "111",
    "port": 3306,
    "db": "test",
    "charset": "utf8"
}

MEMCACHED = {
        "urls": [
            "127.0.0.1:11211"
        ],
        "hostname": "test"
  }

