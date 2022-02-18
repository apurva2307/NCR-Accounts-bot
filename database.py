from decouple import config
import requests, json, jwt, datetime
from dateutil import tz

data_url = config("DATA_URL")
ncr_data_url = config("NCR_DATA_URL")
token = config("TOKEN")


def gen_token(token):
    encodedToken = jwt.encode(
        {
            "name": "shailendra",
            "exp": datetime.datetime.now(tz=tz.gettz("Asia/Kolkata"))
            + datetime.timedelta(seconds=300),
        },
        token,
        algorithm="HS256",
    )
    return encodedToken


def addToDatabase(chat_id, username, first_name):
    registerURL = f"{data_url}/register"
    payload = {
        "chatId": chat_id,
        "username": username,
        "first_name": first_name,
    }
    resp = requests.post(registerURL, json=payload)
    return json.dumps(resp.json())


def get_all_users():
    usersURL = f"{data_url}/getAllUsers"
    encodedToken = gen_token(token)
    headers = {"token": encodedToken}
    allUsers = requests.get(usersURL, headers=headers).json()
    if "telegramUsers" in allUsers.keys():
        return allUsers["telegramUsers"]
    else:
        return json.dumps(allUsers)


def get_single_user(chat_id):
    userURL = f"{data_url}/{chat_id}"
    encodedToken = gen_token(token)
    headers = {"token": encodedToken}
    user = requests.get(userURL, headers=headers).json()
    if "telegramUser" in user.keys():
        return user["telegramUser"]
    else:
        return json.dumps(user)


def delete_single_user(chat_id):
    userURL = f"{data_url}/{chat_id}"
    encodedToken = gen_token(token)
    headers = {"token": encodedToken}
    user = requests.delete(userURL, headers=headers).json()
    if "msg" in user.keys():
        return user["msg"]
    else:
        return json.dumps(user)


def get_owe_data(month):
    dataURL = f"{ncr_data_url}/getData/{month}/OWE"
    encodedToken = gen_token(token)
    headers = {"token": encodedToken}
    res = requests.get(dataURL, headers=headers).json()
    if "monthData" in res.keys():
        return res["monthData"]
    else:
        return res


def get_capex_data(month):
    dataURL = f"{ncr_data_url}/getData/{month}/CAPEX"
    encodedToken = gen_token(token)
    headers = {"token": encodedToken}
    res = requests.get(dataURL, headers=headers).json()
    if "monthData" in res.keys():
        return res["monthData"]
    else:
        return res
