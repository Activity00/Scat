# coding: utf-8
DOWNLOAD_URL = 'localhost'
VERSION = 20171223
HALL_ATTR = 'localhost:10002'
ACCOUNT_PRI_KEY = '^&*#$%()@;'
TOKEN_PRI_KEY = ';@()%$#*&'

MASTER = {
    "root_host": "localhost",
    "root_port": 9999,
    "web_port": 9998
}

SERVERS = {
    'account': {
        'web_port': 10000,
        'db': True,
        'cache': True,
        'app': 'account',
        'log': 'logs/account.log',
        'remote_list': [
            {
                'root_port': 10001,
                'root_name': 'hall'
            }
        ],
    },
    'hall': {
        'name': 'texas_hall',
        'root_port': 10001,
        'web_port': 10002,
        'log': 'logs/hall.log',
        'app': 'hall',
        'db': True,
        'cache': True,
    },
    'game': {
        'name': 'game',
        'web_port': 10003,  # web_socket
        'server': 'servers.game_server',
        'log': 'logs/game.log',
        'db': True,
        'mem': True,
        'app': 'game',
        #'reload': 'app/game/reload',
        'remote_list': [
            {
                'root_port': 10001,
                'root_name': 'hall'
            }
        ],
    }
}

DB = {
    'host': 'localhost',
    'username': 'root',
    'password': 'root',
    'port': 3306,
    'db_name': 'texas',
    "charset": 'utf8'
}

CACHE = {
    'host': '127.0.0.1:6379',
    'port': 6379,
    'host_name': 'texas'
}

