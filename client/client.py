import json
import fire
import requests
from utils import truncate_message, preload, CONFIG_FILE, BASE_URL


MESSAGE_LIMIT = 254


def save_config(key, value):
    config[key] = value
    with open(CONFIG_FILE, 'w') as f_obj:
        json.dump(config, f_obj)


def register(username, password):
    """
    Register user to join rooms and publish messages
    :param username: username to login
    :param password: password to login
    :return: OK if profile creation succeeded, ERR if not
    """
    response = requests.post(f"{BASE_URL}register", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        print('Successfuly registered')
        print(config)
    elif response.status_code == 400:
        print('Username is occupied')
    else:
        print('Error has occured. Try again')
    print(username + str(password))


def login(username, password):
    """
    Login user to get personal token to join rooms
    :param username: username to login
    :param password: password to login
    :return: OK if login succeeded, ERR if not
    """
    response = requests.post(f"{BASE_URL}login", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        print()
        save_config(key='token', value=json.loads(response.text)['token'])
        print(response.text)
    elif response.status_code == 400:
        print(json.loads(response.text)['message'])
    else:
        print('Error has occured. Try again')


def newroom(roomname, nickname=None):
    """
    Create new room
    :param roomname: room identificator, unique in storage
    :param nickname: Optional. Nickname that other users will see.
                    Username will be used by default
    :return: OK if login succeeded, ERR if not
    """
    response = requests.post(f"{BASE_URL}newroom", json={
        "roomname": roomname,
        "username": nickname,
        "token": config['token']
    })
    if response.status_code == 200:
        print('Room has been created. Use "room <roomname> command to enter it"')
    else:
        print('Error has occured. Try again')


def subscribe(roomname, nickname=None):
    """
    Join room
    :param roomname: room identificator, unique in storage
    :param nickname: Optional. Nickname that other users will see.
                    Username will be used by default
    :return: Room history
    """
    response = requests.post(f"{BASE_URL}subscribe", json={
        "roomname": roomname,
        "username": nickname,
        "token": config['token']
    })
    if response.status_code == 200:
        messages = json.loads(response.text).get('messages', [])
        if not messages:
            print('Room history is empty. Write first message')
        else:
            for message in messages:
                print(f"{message.get('sender')}: {message.get('text')}")
    elif response.status_code == 400:
        print(json.loads(response.text).get('message'))
    else:
        print('Error has occured. Try again')


def publish(roomname, message):
    """
    Send message to particular room
    :param roomname: room identificator, unique in storage
    :param message: text message to send
    :return: OK if sending succeeded
    """
    constraint = '\n'
    if len(message.encode('utf-8')) > MESSAGE_LIMIT:
        message = truncate_message(message, MESSAGE_LIMIT)
        constraint += 'However, message was truncated to fit in 254 byte limit'
    response = requests.post(f"{BASE_URL}publish", json={
        "roomname": roomname,
        "message": message,
        "token": config['token']
    })
    if response.status_code == 200:
        print('Message has been sent', end=constraint)
    elif response.status_code == 400:
        print(json.loads(response.text).get('message'))
    else:
        print('Error has occured. Try again')


def room(roomname):
    """
    Changer room to get your rooms' history
    :param roomname: room identificator, unique in storage
    :return: Message history for room <roomname>
    """
    response = requests.post(f"{BASE_URL}room", json={
        "roomname": roomname,
        "token": config['token']
    })
    if response.status_code == 200:
        messages = json.loads(response.text).get('messages', [])
        if not messages:
            print('Room history is empty. Write first message')
        else:
            for message in messages:
                print(f"{message.get('sender')}: {message.get('text')}")
    elif response.status_code == 400:
        print(json.loads(response.text).get('message'))
    else:
        print('Error has occured. Try again')


config = preload()


def main():
    fire.Fire({
        "register": register,
        "login": login,
        "newroom": newroom,
        "subscribe": subscribe,
        "publish": publish,
        "room": room
    })


if __name__ == '__main__':
    main()
