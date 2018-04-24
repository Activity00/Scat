# coding: utf-8


MASTER = {
    "root_host": "localhost",
    "root_port": 9999,
    "web_port": 9998
}

SERVERS = {
    # 'account': {
    #     'net_port': 10000,
    #     'net_protocol': 'tcp',
    #     'db': True,
    #     'mem': True,
    #     'server': 'servers.account_server',
    #     'log': 'logs/account.log'
    # },
    'hall_1': {
        'name': '三组广场',
        'root_port': 10001,
        'web_port': 10002,
        'server': 'servers.hall_server',
        'log': 'logs/hall.log',
        'db': True,
        'cache': True,
    },
    'game_1': {
        'web_port': 10003,  # web_socket
        'server': 'servers.game_server',
        'log': 'logs/game.log',
        'db': True,
        'mem': True,
        'reload': 'app/game/reload',
        'remote_list': [
            {
                'root_port': 10001,
                'root_name': 'hall_1'
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
    'urls': [
        '127.0.0.1:6379'
    ],
    'host_name': 'texas'
}

