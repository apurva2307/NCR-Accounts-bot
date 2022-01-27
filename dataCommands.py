from database import get_owe_data
from helpers import *


def execute_data_command(command, chat_id):
    command = command.lower()

    if command[0:4] == "owe " and len(command) >= 13 and len(command) < 15:
        data = get_owe_data(command[4:9].upper())
        if "msg" in data.keys():
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        data1 = data["data1"]
        pu = command[10:].upper()
        if pu not in data1.keys():
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        if pu in data1.keys():
            puData = data1[pu]["toEndActuals"]
            msg = ""
            for index, value in enumerate(puData):
                if index == 11:
                    msg += f"Total: {value} thousand\n"
                else:
                    msg += f"D{index+3}: {value} thousand\n"
            broadcast_msg(chat_id, msg)
    else:
        broadcast_msg(chat_id, "No such command exists..")
