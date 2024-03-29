from decouple import config
from flask import Flask, request
import requests, json
from adminCommands import execute_admin_command
from helpers import *
from commands import *
from database import addToDatabase, delete_single_user, get_single_user
from dataCommands import execute_owe_command
from capexCommands import execute_capex_command

app = Flask(__name__)
API_KEY = config("API_KEY")
API_URL = f"https://api.telegram.org/bot{API_KEY}"


@app.route("/set")
def set_webhook():
    url = config("WEB_URL")
    webhook_url = f"{url}/{API_KEY}"
    setWebhook = f"{API_URL}/setWebhook"
    options = {
        "url": webhook_url,
        "allowed_updates": ["message"],
        "drop_pending_updates": True,
    }
    requests.post(setWebhook, json=options)
    return "Webhook has been set."


@app.route("/clear")
def delete_webhook():
    deleteWebhook = f"{API_URL}/deleteWebhook"
    options = {"drop_pending_updates": True}
    requests.post(deleteWebhook, json=options)
    return "Webhook has been removed."


@app.route("/trial", methods=["POST"])
def auto_msg():
    req = request.get_json()
    print("trial>>", req)
    print("header>>", request.headers["token"])
    msg = req["msg"]
    broadcast_admin(msg)
    return "Reminder invoked."


@app.route("/get")
def get_webhook_info():
    getWebhookInfo = f"{API_URL}/getWebhookInfo"
    resp = requests.get(getWebhookInfo)
    return json.dumps(resp.json()["result"])


@app.route("/")
def hello_world():
    return "Welcome!! NCR Accounts bot."


@app.route("/" + API_KEY, methods=["POST"])
def getMessage():
    req = request.get_json()
    print("req>>", req)
    chat_id, txt, first_name, username = parse_request(req)
    try:
        if "text" in req["message"].keys():
            if txt == "/start" or txt == "/subscribe":
                response = addToDatabase(chat_id, username, first_name)
                json_msg = json.loads(response)
                if "msg" in json_msg.keys():
                    if (
                        json_msg["msg"]
                        == f"chat_Id {chat_id} already exists for NCR_Accounts bot."
                    ):
                        broadcast_msg(
                            chat_id,
                            "You have already subscribed for NCR_Accounts updates service.",
                        )
                    else:
                        broadcast_msg("44114772", json.dumps(json_msg))
                else:
                    broadcast_msg(
                        chat_id,
                        "Thanks for subscribing for NCR_Accounts updates service. Kindly wait for approval from admin, then only you can use services of this bot.",
                    )
                broadcast_admin(response)
                broadcast_admin(chat_id)
                broadcast_admin(f"@{username}")
            elif txt == "/unsubscribe":
                response = delete_single_user(chat_id)
                if (
                    response
                    == f"chat Id {chat_id} for NCR_Accounts bot is successfully deleted."
                ):
                    broadcast_msg(
                        chat_id,
                        "You are successfully unsubscribed from NCR_Accounts updates service.",
                    )
                broadcast_admin(response)
                broadcast_admin(chat_id)
                broadcast_admin(f"@{username}")
            else:
                res = get_single_user(chat_id)
                # res = {"role": "admin"}
                if not res or type(res) == str:
                    return "!", 200
                role = res["role"]
                if role == "banned":
                    broadcast_msg(
                        chat_id,
                        "You are not authorized to access services of this bot. Kindly contact admin @Dream_Big18 for getting access.",
                    )
                elif role == "user" or role == "admin":
                    if is_command(txt):
                        execute_command(txt, chat_id)
                    else:
                        adminCmdExecuted = "No"
                        if role == "admin":
                            adminCmdExecuted = execute_admin_command(txt, chat_id)
                        unit = "NCR"
                        if txt.upper().startswith("JHS "):
                            unit = "JHS"
                            txt = txt[4:]
                        elif txt.upper().startswith("AGC "):
                            unit = "AGC"
                            txt = txt[4:]
                        elif txt.upper().startswith("PRYJ "):
                            unit = "PRYJ"
                            txt = txt[5:]
                        if adminCmdExecuted == "No":
                            if txt.lower().startswith("owe") or txt.lower().startswith(
                                "get"
                            ):
                                execute_owe_command(txt, chat_id, unit)
                            elif txt.lower().startswith("capex "):
                                execute_capex_command(txt, chat_id)
                            else:
                                broadcast_msg(chat_id, "No such command exists..")
    except Exception as e:
        print(e)
        broadcast_admin(f"{e}")
        broadcast_msg(
            chat_id,
            "Something went wrong during execution of command, please try again later.",
        )
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config("PORT") if config("PORT") else 5000, debug=True)
