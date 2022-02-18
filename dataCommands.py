from database import get_owe_data, get_capex_data
from getExcelCommands import make_excel
from helpers import *
from dataHelpers import get_data_type_two
from capexCommands import execute_capex_command
import os


def execute_data_command(command, chat_id):
    command = command.upper()
    options = ["BUD", "BP", "COPPY", "VAR", "VARBP", "VARCOPPY", "BUDUTIL"]
    if command[0:4] == "OWE ":
        cmd = command.split(" ")
        if len(cmd[1]) > 5 or len(cmd[1]) < 5:
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
            puData1 = data1["STAFF"]["toEndActuals"]
            puData1Util = data1["STAFF"]["budgetUtilization"]
            puData2 = data1["NONSTAFF"]["toEndActuals"]
            puData2Util = data1["NONSTAFF"]["budgetUtilization"]
            puData3 = data1["NET"]["toEndActuals"]
            puData3Util = data1["NET"]["budgetUtilization"]
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
                    otheroptions = ["CREDIT", "STAFF", "NONSTAFF", "GROSS", "NET"]
                    title = f"Actuals for {pu} (Budget Util.) >>"
                    if pu in otheroptions:
                        title = f"{pu} Total Actuals (Budget Util.) >>"
                    message = get_data_type_two(title, puData, puDataUtil, True)
                    broadcast_msg(chat_id, message)
                if pu == "BUD":
                    puData = data1["NET"]["budget"]
                    puDataUtil = data1["NET"]["budgetUtilization"]
                    message = get_data_type_two(
                        "Net Budget (Budget Util.) >>", puData, puDataUtil, True
                    )
                    broadcast_msg(chat_id, message)
                if pu == "BP":
                    puData = data1["NET"]["toEndBp"]
                    puDataUtil = data1["NET"]["varAcBpPercent"]
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
                    message = get_data_type_two(
                        "Variation AC over BP absolute (Percentage) >>",
                        puData1,
                        puData2,
                        True,
                    )
                    broadcast_msg(chat_id, message)
                    message = get_data_type_two(
                        "Variation AC over COPPY absolute (Percentage) >>",
                        puData3,
                        puData4,
                        True,
                    )
                    broadcast_msg(chat_id, message)
    elif command[0:6] == "CAPEX ":
        cmd = command.split(" ")
        if len(cmd[1]) > 5 or len(cmd[1]) < 5:
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        data = get_capex_data(cmd[1])
        if not data:
            broadcast_msg(chat_id, "No data is available for given input.")
            return
        if "msg" in data.keys():
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        data1 = data["data1"]
        execute_capex_command(data1, cmd, chat_id)
    elif command[:9] == "GETEXCEL ":
        cmd = command.split(" ")
        if len(cmd[1]) > 5 or len(cmd[1]) < 5:
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        data = get_owe_data(cmd[1])
        if not data:
            broadcast_msg(chat_id, "No data is available for given input.")
            return
        if "msg" in data.keys():
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        if cmd[1][:3] in ["JAN", "FEB", "MAR"]:
            lastYear = int(cmd[1][3:]) - 1
        else:
            lastYear = cmd[1][3:]
        data1 = data["data1"]
        print(lastYear)
        lastYearData = get_owe_data(f"MAR{lastYear}")
        print(lastYearData)
        if cmd[2] not in data1.keys():
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        make_excel(cmd[1], cmd[2], data1, lastYearData)
        if os.path.isfile(f"{cmd[2]}.xlsx"):
            sendFile(chat_id, "excel", f"{cmd[2]}.xlsx", f"{cmd[2]}.xlsx")
            os.remove(f"{cmd[2]}.xlsx")
        else:
            broadcast_msg(chat_id, "Something went wrong. Please try again later.")
    else:
        broadcast_msg(chat_id, "No such command exists..")
