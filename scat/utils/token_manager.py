# coding: utf-8

"""
@author: 武明辉 
@time: 2018/5/10 13:10
"""
import time
from hashlib import md5


class TokenManager:
    def __init__(self, token_pri_key):
        self.token_pri_key = token_pri_key
        self.tokens = {}    # token: token_info
        self.player_token_mapping = {}    # player_id: token

    def exist(self, token):
        return token in self.tokens

    def produce_token(self, player_id, life_time):
        token = self.player_token_mapping.get(player_id)
        if token:
            self.del_token(token)
        time_stamp = time.time()
        token = md5((player_id + time_stamp + self.token_pri_key).encode()).hexdigest()
        self.tokens[token] = {
            'player_id': player_id,
            'time': time_stamp,
            'life_time': life_time
        }
        return token

    def del_token(self, token):
        if token in self.tokens:
            player_id = self.tokens.get('player_id')
            del self.player_token_mapping[player_id]
            del self.tokens[token]

    def is_token_valid(self, token):
        token_info = self.tokens.get(token)
        return True if token_info['time'] + token_info['life_time'] > time.time() else False

    def get_user_id_from_token(self, token):
        token_info = self.tokens.get(token)
        if not token_info:
            return None
        return token_info['player_id']

    def get_token_from_user_id(self, player_id):
        return self.player_token_mapping.get(player_id)


if __name__ == '__main__':
    pass
