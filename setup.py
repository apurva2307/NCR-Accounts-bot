import os
import requests
from flask import Flask

API_KEY = os.environ["API_KEY"]
server = Flask(__name__)


def broadcast_messages(list_of_groups, msg):
    for group in list_of_groups:
        to_url = f"https://api.telegram.org/bot{API_KEY}/sendMessage?chat_id={group}&text={msg}&parse_mode=HTML"
        resp = requests.get(to_url)
        print(resp.text)


broadcast_messages(["641792797"], "HI from bot")


@server.route("/")
def webhook():
    return "!", 200
