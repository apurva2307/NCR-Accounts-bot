from database import get_owe_data
from helpers import *


def execute_data_command(command, chat_id):
    command = command.lower()

    if command[0:4] == "owe ":
        cmd = command.upper().split(" ")
        if len(cmd[1]) > 5:
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        data = get_owe_data(cmd[1])
        if not data:
            broadcast_msg(chat_id, "No data is available for given input.")
            return
        if "msg" in data.keys():
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        data1 = data["data1"]
        if len(cmd) == 2:
            puData1 = data1["Staff Cost"]["toEndActuals"]
            puData1Util = data1["Staff Cost"]["budgetUtilization"]
            puData2 = data1["Non-Staff Cost"]["toEndActuals"]
            puData2Util = data1["Non-Staff Cost"]["budgetUtilization"]
            puData3 = data1["Net"]["toEndActuals"]
            puData3Util = data1["Net"]["budgetUtilization"]
            msg = ""
            for index, value in enumerate(puData1):
                if index == 0:
                    msg += f"Staff Cost Actuals (Budget Util.) >>\nD{index+3}: {value} thousand ({puData1Util[index]}%)\n"
                elif index == 11:
                    msg += f"Total: {value} thousand ({puData1Util[index]}%)\n"
                    broadcast_msg(chat_id, msg)
                    msg = ""
                else:
                    msg += f"D{index+3}: {value} thousand ({puData1Util[index]}%)\n"
            for index, value in enumerate(puData2):
                if index == 0:
                    msg += f"Non-Staff Cost Actuals (Budget Util.) >>\nD{index+3}: {value} thousand ({puData2Util[index]}%)\n"
                elif index == 11:
                    msg += f"Total: {value} thousand ({puData2Util[index]}%)\n"
                    broadcast_msg(chat_id, msg)
                    msg = ""
                else:
                    msg += f"D{index+3}: {value} thousand ({puData2Util[index]}%)\n"
            for index, value in enumerate(puData3):
                if index == 0:
                    msg += f"Net Total Actuals (Budget Util.) >>\nD{index+3}: {value} thousand ({puData3Util[index]}%)\n"
                elif index == 11:
                    msg += f"Total: {value} thousand ({puData3Util[index]}%)\n"
                    broadcast_msg(chat_id, msg)
                    msg = ""
                else:
                    msg += f"D{index+3}: {value} thousand ({puData3Util[index]}%)\n"
        if len(cmd) >= 3:
            pu = cmd[2]
            if pu not in data1.keys():
                broadcast_msg(chat_id, "Invalid input provided.")
                return
            if len(cmd) == 3:
                if pu in data1.keys():
                    puData = data1[pu]["toEndActuals"]
                    msg = ""
                    for index, value in enumerate(puData):
                        if index == 11:
                            msg += f"Total: {value} thousand\n"
                        else:
                            msg += f"D{index+3}: {value} thousand\n"
                    broadcast_msg(chat_id, msg)
            if len(cmd) == 4:
                if cmd[3] == "VAR":
                    puData1 = data1[pu]["varAcBp"]
                    puData2 = data1[pu]["varAcBpPercent"]
                    puData3 = data1[pu]["varAcCoppy"]
                    puData4 = data1[pu]["varAcCoppyPercent"]
                    msg = ""
                    for index, value in enumerate(puData1):
                        if index == 0:
                            msg += f"Variation AC over BP absolute >>\nD{index+3}: {value} thousand\n"
                        elif index == 11:
                            msg += f"Total: {value} thousand\n"
                            broadcast_msg(chat_id, msg)
                            msg = ""
                        else:
                            msg += f"D{index+3}: {value} thousand\n"
                    for index, value in enumerate(puData2):
                        if index == 0:
                            msg += f"Variation AC over BP percent >>\nD{index+3}: {value}%\n"
                        elif index == 11:
                            msg += f"Total: {value}%\n"
                            broadcast_msg(chat_id, msg)
                            msg = ""
                        else:
                            msg += f"D{index+3}: {value}%\n"
                    for index, value in enumerate(puData3):
                        if index == 0:
                            msg += f"Variation AC over COPPY absolute >>\nD{index+3}: {value} thousand\n"
                        elif index == 11:
                            msg += f"Total: {value} thousand\n"
                            broadcast_msg(chat_id, msg)
                            msg = ""
                        else:
                            msg += f"D{index+3}: {value} thousand\n"
                    for index, value in enumerate(puData4):
                        if index == 0:
                            msg += f"Variation AC over COPPY percent >>\nD{index+3}: {value}%\n"
                        elif index == 11:
                            msg += f"Total: {value}%\n"
                            broadcast_msg(chat_id, msg)
                            msg = ""
                        else:
                            msg += f"D{index+3}: {value}%\n"

    else:
        broadcast_msg(chat_id, "No such command exists..")
