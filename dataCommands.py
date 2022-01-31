from database import get_owe_data
from helpers import *
from dataHelpers import get_data_type_two


def execute_data_command(command, chat_id):
    command = command.lower()
    options = ["BUD", "BP", "COPPY", "VAR", "VARBP", "VARCOPPY", "BUDUTIL"]
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
            message = get_data_type_two(
                "Staff Cost Actuals (Budget Util.) >>", puData1, puData1Util, True
            )
            broadcast_msg(chat_id, message)
            message = get_data_type_two(
                "Non-Staff Cost Actuals (Budget Util.) >>", puData2, puData2Util, True
            )
            broadcast_msg(chat_id, message)
            message = get_data_type_two(
                "Net Total Actuals (Budget Util.) >>", puData3, puData3Util, True
            )
            broadcast_msg(chat_id, message)

        if len(cmd) >= 3:
            pu = cmd[2]
            if pu not in data1.keys() and pu not in options:
                broadcast_msg(chat_id, "Invalid input provided.")
                return
            if len(cmd) == 3:
                if pu in data1.keys():
                    puData = data1[pu]["toEndActuals"]
                    puDataUtil = data1[pu]["budgetUtilization"]
                    message = get_data_type_two(
                        "Net Total Actuals (Budget Util.) >>", puData, puDataUtil, True
                    )
                    broadcast_msg(chat_id, message)
                if pu == "BUD":
                    puData = data1["Net"]["budget"]
                    puDataUtil = data1["Net"]["budgetUtilization"]
                    message = get_data_type_two(
                        "Net Budget (Budget Util.) >>", puData, puDataUtil, True
                    )
                    broadcast_msg(chat_id, message)
                if pu == "BP":
                    puData = data1["Net"]["toEndBp"]
                    puDataUtil = data1["Net"]["varAcBpPercent"]
                    message = get_data_type_two(
                        "Net BP (Var. BP in %) >>", puData, puDataUtil, True
                    )
                    broadcast_msg(chat_id, message)
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
