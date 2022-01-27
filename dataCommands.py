from database import get_owe_data
from helpers import *


def execute_data_command(command, chat_id):
    command = command.lower()

    if command[0:4] == "owe " and len(command) >= 13:
        data = get_owe_data(command[4:9])
        data1 = data["data1"]
        puData = data1[command[10:]]
        broadcast_msg(chat_id, f"{puData}")
    else:
        broadcast_msg(chat_id, "No such data command exists..")
