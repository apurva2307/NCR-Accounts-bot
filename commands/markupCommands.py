from os import getenv
import requests
from helpers.markupHelpers import answer_callback_query
from helpers.helpers import broadcast_msg
from constants.constants import API_URL
from helpers.adminSection import *


to_url = f"{API_URL}/sendMessage"
def execute_markup(chat_id, command):
    cmd = command.lower()
    if cmd == "test":
        payload = {
            "chat_id": chat_id,
            "text": "Testing markup commands\nChoose any option:",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "Option A", "callback_data": "a"},
                        {"text": "Option B", "callback_data": "b"},
                    ],
                    [{"text": "Option C", "callback_data": "c"}],
                ]
            },
        }
        resp = requests.post(to_url, json=payload)
        return resp
    elif cmd == "staff":
        payload = {
            "chat_id": chat_id,
            "text": "To get various statistics, choose any option:",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "Staff Strength", "callback_data": "OnRoll"}
                    ],
                    [{"text": "Rotation Due", "callback_data": "Rotation"}]
                ]
            },
        }
        resp = requests.post(to_url, json=payload)
        return resp
    elif cmd == "officer":
        payload = {
            "chat_id": chat_id,
            "text": "To get various statistics, choose any option:",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {"text": "Officer Strength", "callback_data": "OnRoll_Officer"}
                    ],
                    [{"text": "Rotation Due", "callback_data": "Rotation_Officer"}],
                    [{"text": "Post Codes", "callback_data": "Post_Code"}]
                ]
            },
        }
        resp = requests.post(to_url, json=payload)
        return resp
    else:
        broadcast_msg(chat_id, "This keyword not implemented yet.")
        return


def execute_markup_query(chat_id, query_id, reply_markup, markup_header, data):
    if data:
        if data in ["a", "b", "c"]:
            broadcast_msg(chat_id, f"You chose option {data.upper()}")
            answer_callback_query(query_id, "Done")
        elif data == "OnRoll":
            payload = {
                "chat_id": chat_id,
                "text": "To get staff Onroll position, choose any option:",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": "SSO", "callback_data": "SSO"},
                            {"text": "JAA", "callback_data": "JAA"},
                        ],
                        [
                            {"text": "AA", "callback_data": "AA"},
                            {"text": "AC", "callback_data": "AC"},
                        ],
                        [{"text": "ALL", "callback_data": "ALL"}],
                    ]
                },
            }
            resp = requests.post(to_url, json=payload)
            return resp
        elif markup_header == "To get staff Onroll position, choose any option:":
            onroll = get_staff_strength("Staff", data)
            broadcast_msg(chat_id, onroll)
            answer_callback_query(query_id, "Done.")
        elif markup_header == "To get officers Onroll position, choose any option:":
            onroll = get_staff_strength("Officer", data)
            broadcast_msg(chat_id, onroll)
            answer_callback_query(query_id, "Done.")
        elif markup_header == "To get post codes of various posts, choose any option:":
            codes = get_post_codes(data)
            broadcast_msg(chat_id, codes)
            answer_callback_query(query_id, "Done.")
        elif data == "Rotation":
            res= get_staff_rotation_status()
            broadcast_msg(chat_id, res)
            answer_callback_query(query_id, "Done.")
        elif data == "Rotation_Officer":
            res= get_officer_rotation_status()
            broadcast_msg(chat_id, res)
            answer_callback_query(query_id, "Done.")
        elif data == "OnRoll_Officer":
            payload = {
                "chat_id": chat_id,
                "text": "To get officers Onroll position, choose any option:",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": "HAG", "callback_data": "HAG"},
                            {"text": "SAG", "callback_data": "SAG"},
                            {"text": "JAG/SG", "callback_data": "JAG/SG"},
                        ],
                        [
                            {"text": "SS", "callback_data": "SS"},
                            {"text": "JS", "callback_data": "JS"},
                            {"text": "GRP-B", "callback_data": "Group-B"},
                            {"text": "ALL", "callback_data": "ALL"},
                        ],
                    ]
                },
            }
            resp = requests.post(to_url, json=payload)
            return resp
        elif data == "Post_Code":
            payload = {
                "chat_id": chat_id,
                "text": "To get post codes of various posts, choose any option:",
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": "HAG", "callback_data": "HAG"},
                            {"text": "SAG", "callback_data": "SAG"},
                            {"text": "JAG/SG", "callback_data": "JAG/SG"},
                        ],
                        [
                            {"text": "SS", "callback_data": "SS"},
                            {"text": "JS", "callback_data": "JS"},
                            {"text": "GRP-B", "callback_data": "Group-B"},
                            {"text": "ALL", "callback_data": "ALL"},
                        ],
                    ]
                },
            }
            resp = requests.post(to_url, json=payload)
            return resp
        
if __name__ == "__main__":
    print("hi")