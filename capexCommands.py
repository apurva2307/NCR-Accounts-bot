from datafromPandas import get_data
import pandas
from helpers import broadcast_msg
from puPhList import getPHs
from datafromPandas import *


def execute_capex_command(command, chat_id):
    cmd = command.upper().split(" ")
    if len(cmd[1]) > 5 or len(cmd[1]) < 5:
        broadcast_msg(chat_id, "Invalid input provided.")
        return
    data, error = get_data(cmd[1])
    if error:
        return broadcast_msg(chat_id, error)
    if isinstance(data, pandas.DataFrame) and not error:
        if len(cmd) == 2:
            ncrData = get_unit_data(data, "NCR")
            totalData = get_phdata(ncrData, "Total Source wise 11 to 65")
            msg = "Source of fund wise upto month actuals Total (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
            for key, value in totalData["Total Source wise 11 to 65"].items():
                actuals = value[-2]
                budUtil = value[-1]
                msg += f"{key}: {actuals} ({budUtil}%)\n"
            for index, val in (
                ncrData[ncrData["Allocation"] == "Total EBR-IF"]
            ).iterrows():
                values = list(val)
                ebrIfTotal = values[-2]
                ebrIfTotalUtil = values[-1]
                msg += f"\nEBR-IF: {ebrIfTotal} ({ebrIfTotalUtil}%)"
            for index, val in (data[data["Allocation"] == "Total EBR-P"]).iterrows():
                values = list(val)
                ebrPTotal = values[3]
                ebrPTotalUtil = values[4]
                msg += f"\nEBR-P: {ebrPTotal} ({ebrPTotalUtil}%)"
            gTotal = list(ncrData.iloc[-2])[-2]
            gTotalUtil = list(ncrData.iloc[-2])[-1]
            msg += f"\nGrand Total: {gTotal} ({gTotalUtil}%)"
            broadcast_msg(chat_id, msg)
        elif len(cmd) > 2:
            phList = getPHs()
            if cmd[2] not in phList or cmd[2] in ["G-TOTAL", "TOTAL"]:
                broadcast_msg(chat_id, "Invalid input provided.")
                return
            if len(cmd) == 3:
                ncrData = get_unit_data(data, "NCR")
                if cmd[2] in phList:
                    phData = get_phdata(ncrData, cmd[2])
                    msg = f"Source of fund wise upto month actuals for {cmd[2]} (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
                    for key, value in phData.items():
                        actuals = value[-2]
                        budUtil = value[-1]
                        msg += f"{key}: {actuals} ({budUtil}%)\n"
                    broadcast_msg(chat_id, msg)
                elif cmd[2] == "BUDGET":
                    totalData = get_phdata(ncrData, "Total Source wise 11 to 65")
                    msg = f"Source of fund wise total Budget Grant>\n <b><i>Figures in Thousand</i></b>\n"
                    for key, value in totalData["Total Source wise 11 to 65"].items():
                        budGrant = value[-3]
                        msg += f"{key}: {budGrant}\n"
                    for index, val in (
                        ncrData[ncrData["Allocation"] == "Total EBR-IF"]
                    ).iterrows():
                        values = list(val)
                        ebrIfBud = values[-3]
                    for index, val in (
                        data[data["Allocation"] == "Total EBR-P"]
                    ).iterrows():
                        values = list(val)
                        ebrPBud = values[2]
                    gTotalBud = list(ncrData.iloc[-2])[-3]
                    msg += f"EBR-IF: {ebrIfBud}\n"
                    msg += f"EBR-P: {ebrPBud}\n"
                    msg += f"G-TOTAL: {gTotalBud}\n"
                    broadcast_msg(chat_id, msg)
                # else:
                #     msg = f"Upto month actuals for {cmd[2]} (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
                #     for key in data1.keys():
                #         if key in ["TOTAL", "G-TOTAL", "EBR-IF", "EBR-P"]:
                #             continue
                #         else:
                #             if cmd[2] in data1[key].keys():
                #                 msg += f"{key}: {data1[key][cmd[2]]['NCR'][-2]} ({data1[key][cmd[2]]['NCR'][-1]}%)\n"
                #     # return msg
                #     broadcast_msg(chat_id, msg)
            elif len(cmd) == 4:
                totalData = data1[cmd[2]]
                if cmd[3] not in ["NCR", "OPEN", "CON"]:
                    broadcast_msg(chat_id, "Invalid input provided.")
                    return
                ofUnit = (
                    "Openline"
                    if cmd[3] == "OPEN"
                    else "Construction including NCRPU"
                    if cmd[3] == "CON"
                    else "Whole NCR"
                )
                msg = f"Source of fund wise upto month actuals for {cmd[2]} of {ofUnit} (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
                for key, value in totalData.items():
                    actuals = value[cmd[3]][-2]
                    budUtil = value[cmd[3]][-1]
                    msg += f"{key}: {actuals} ({budUtil}%)\n"
                # return msg
                broadcast_msg(chat_id, msg)
                return
            else:
                broadcast_msg(chat_id, "Invalid input provided.")
    else:
        broadcast_msg(chat_id, "Invalid input provided.")


if __name__ == "__main__":
    from capexData import getCapexData

    data1 = getCapexData()["monthData"]["data1"]
    res = execute_capex_command(data1, ["CAPEX", "DEC21", "BUDGET"], "567567")
    print(res)
