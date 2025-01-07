import requests
from constants.constants import API_URL


def parse_callback_query(req):
    chat_id = req["callback_query"]["from"]["id"]
    reply_markup = req["callback_query"]["message"]["reply_markup"]
    markup_header = req["callback_query"]["message"]["text"]
    markup_msg_id = req["callback_query"]["message"]["message_id"]
    if "data" in req["callback_query"].keys():
        data = req["callback_query"]["data"]
    else:
        data = None
    query_id = req["callback_query"]["id"]
    return chat_id, query_id, markup_msg_id, reply_markup, markup_header, data


def answer_callback_query(query_id, text):
    to_url = f"{API_URL}/answerCallbackQuery"
    payload = {
        "callback_query_id": query_id,
        "text": text
    }
    resp = requests.post(to_url, json=payload)