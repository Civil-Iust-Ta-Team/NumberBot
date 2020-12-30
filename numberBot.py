import requests
import json

url = "https://api.telegram.org/bot1312813885:AAG-rLhOVFu8R67mN08Bq5JsUSARFQXOiN0/"


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


if __name__ == "__main__":
    data = get_all_updates()
    last = last_update(data)
    chat_id = get_chat_id(last)
    send_message(chat_id, 'salam')
    send_photo(chat_id, open('120077896.png', 'rb'))
    print()
