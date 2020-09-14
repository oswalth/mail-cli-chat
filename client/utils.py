import os
import json

CONFIG_FILE = './config.json'
BASE_URL = 'https://whispering-oasis-17943.herokuapp.com/'


def truncate_message(message, limit):
    i = 0
    while True:
        try:
            message = message.encode(
                'utf-8')[:(limit - i)].decode('utf-8')
        except:
            i += 1
            pass
        else:
            break
    return message


def preload():
    if not os.path.isfile(CONFIG_FILE):
        config = {'token': None}
        with open(CONFIG_FILE, 'w') as f_obj:
            json.dump(config, f_obj)
    else:
        with open(CONFIG_FILE) as f_obj:
            config = json.load(f_obj)
    return config
