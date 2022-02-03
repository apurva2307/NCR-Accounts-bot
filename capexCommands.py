from helpers import broadcast_msg
from puPhList import getPHs


def execute_capex_command(data1, cmd, chat_id):
    if len(cmd) == 2:
        totalData = data1["TOTAL"]
        msg = "Source of fund wise upto month actuals Total (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
        for key, value in totalData.items():
            actuals = value["NCR"][-2]
            budUtil = value["NCR"][-1]
            msg += f"{key}: {actuals} ({budUtil}%)\n"
        gTotal = data1["G-TOTAL"]["NCR"][-2]
        gTotalUtil = data1["G-TOTAL"]["NCR"][-1]
        msg += f"\nGrand Total: {gTotal} ({gTotalUtil}%)"
        # return msg
        broadcast_msg(chat_id, msg)
    elif len(cmd) > 2:
        phList = getPHs()
        if cmd[2] not in phList and cmd[2] not in data1["TOTAL"].keys():
            broadcast_msg(chat_id, "Invalid input provided.")
            return
        if len(cmd) == 3:
            if cmd[2] in phList:
                totalData = data1[cmd[2]]
                msg = f"Source of fund wise upto month actuals for {cmd[2]} (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
                for key, value in totalData.items():
                    actuals = value["NCR"][-2]
                    budUtil = value["NCR"][-1]
                    msg += f"{key}: {actuals} ({budUtil}%)\n"
                # return msg
                broadcast_msg(chat_id, msg)
            else:
                msg = f"Upto month actuals for {cmd[2]} (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
                for key in data1.keys():
                    if key in ["TOTAL", "G-TOTAL", "EBR-IF", "EBR-P"]:
                        continue
                    else:
                        if cmd[2] in data1[key].keys():
                            msg += f"{key}: {data1[key][cmd[2]]['NCR'][-2]} ({data1[key][cmd[2]]['NCR'][-1]}%)\n"
                # return msg
                broadcast_msg(chat_id, msg)
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
    res = execute_capex_command(data1, ["CAPEX", "DEC21", "DRF"], "567567")
    print(res)
