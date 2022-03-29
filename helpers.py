import requests, json, pickle
from decouple import config
from database import get_all_users

API_KEY = config("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_KEY}"


def sendFile(chat_id, type, file_path, file_name):
    url = f"{API_URL}/send"
    payload = {"chat_id": chat_id}
    url = f"{url}Document"
    doc_type = ""
    if type == "txt":
        doc_type = "text/plain"
    elif type == "excel":
        doc_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif type == "pdf":
        doc_type = "application/pdf"
    files = [
        (
            "document",
            (
                f"{file_name}",
                open(f"{file_path}", "rb"),
                f"{doc_type}",
            ),
        )
    ]
    resp = requests.request("POST", url, data=payload, files=files)
    return json.dumps(resp.json())


def broadcast_all(func, chat_ids, *args):
    for chat_id in chat_ids:
        func(chat_id, *args)


def broadcast_msg(chat_id, msg):
    to_url = f"{API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
    resp = requests.post(to_url, json=payload)
    return json.dumps(resp.json())


def broadcast_items(chat_id, item, type):
    to_url = f"{API_URL}/send{type}"
    if type == "Sticker":
        payload = {"chat_id": chat_id, "sticker": item}
    if type == "Photo":
        payload = {"chat_id": chat_id, "photo": item}
    if type == "Document":
        payload = {"chat_id": chat_id, "document": item}
    resp = requests.post(to_url, json=payload)
    return json.dumps(resp.json())


def parse_request(req):
    chat_id = req["message"]["chat"]["id"]
    if "text" in req["message"].keys():
        txt = req["message"]["text"]
        pickle.dumps(txt)
    elif "sticker" in req["message"].keys():
        txt = req["message"]["sticker"]["file_id"]
    elif "document" in req["message"].keys():
        txt = req["message"]["document"]["file_id"]
    elif "photo" in req["message"].keys():
        txt = req["message"]["photo"][0]["file_id"]
    first_name = req["message"]["chat"]["first_name"]
    if "username" in req["message"]["chat"].keys():
        username = req["message"]["chat"]["username"]
    else:
        username = "Not provided"
    return chat_id, txt, first_name, username


def broadcastToAll(msg):
    users = get_all_users()
    for user in users:
        broadcast_msg(user["chatId"], msg)


def broadcast_admin(msg):
    broadcast_msg("44114772", msg)
