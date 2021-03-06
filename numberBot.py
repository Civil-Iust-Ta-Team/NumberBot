import requests
import json
import random
from flask import request
from flask import Flask
from flask import Response
import os
url = "https://api.telegram.org/bot1312813885:AAG-rLhOVFu8R67mN08Bq5JsUSARFQXOiN0/"

app = Flask(__name__)


def get_all_updates():
    global url
    response = requests.get(url + 'getUpdates')
    return response.json()


def last_update(data):
    result = data['result']
    last_index_number = len(result) - 1
    return result[last_index_number]


def get_chat_id(update):
    return update['message']['chat']['id']


def send_message(chat_id, text):
    global url
    send_data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url + 'sendMessage', send_data)
    return response


def send_photo(chat_id, photo):
    global url
    data = {'chat_id': chat_id}
    myfile = {'photo': photo}
    response = requests.post(url + 'sendPhoto', data=data, files=myfile)
    return response


def game(target, n):
    target = int(target)
    n = int(n)
    if n > target:
        return 'kuchektr ast'
    elif n < target:
        return 'bozorgtr ast'
    else:
        return 'barabar'


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chatid = str(msg['message']['chat']['id'])
        message = msg['message'].get('text', '')
        if message == '/start':
            send_message(chatid, 'salam khsoh amdid')
            send_message(chatid, 'baraie bazi krdn shoro ro bfres')
            olderCommands = read_json()
            olderCommands[chatid] = []
            write_json(olderCommands)
        elif message.find('shoro') != -1:
            olderCommands = read_json()
            olderCommands[chatid] = []
            olderCommands.get(chatid).append(random.randrange(100, 1000))
            write_json(olderCommands)
            send_message(chatid, 'adad entekhab shod hds bzn, adad bein 100 va 1000 ast.')
        elif message.isdigit():
            olderCommands = read_json()
            list_user = olderCommands.get(chatid, [])
            if isinstance(list_user, list):
                print(len(list_user))
            if not isinstance(list_user, list):
                send_message(chatid, 'etelat nadorst ast')
            elif len(list_user) == 1:
                print('ok')
                result = game(list_user[0], message)
                if result == 'barabar':
                    send_message(chatid, 'hooora dorost hds zdid')
                    olderCommands[chatid] = []
                else:
                    send_message(chatid, result)

        return Response('ok', status=200)

    else:
        return '<h1>salam aleykom<h1>'


def write_json(data, fileName='response.json'):
    with open(fileName, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(fileName='response.json'):
    with open(fileName, 'r') as f:
        dic = json.load(f)
    return dic


if __name__ == "__main__":
    olderCommands = {}
    write_json(olderCommands)
    # data = get_all_updates()
    # last = last_update(data)
    # chat_id = get_chat_id(last)
    # send_message(chat_id, 'salam')
    # send_photo(chat_id, open('120077896.png', 'rb'))
    # print()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
