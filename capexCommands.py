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
        if len(cmd) == 3:
            phList = getPHs()
            if cmd[2] not in phList:
                broadcast_msg(chat_id, "Invalid input provided.")
                return
            totalData = data1[cmd[2]]
            msg = f"Source of fund wise upto month actuals for {cmd[2]} (Budget Utilization)>\n <b><i>Figures in Thousand</i></b>\n"
            for key, value in totalData.items():
                actuals = value["NCR"][-2]
                budUtil = value["NCR"][-1]
                msg += f"{key}: {actuals} ({budUtil}%)\n"
            # return msg
            broadcast_msg(chat_id, msg)
            return
    else:
        broadcast_msg(chat_id, "Invalid input provided.")


if __name__ == "__main__":
    from capexData import getCapexData

    data1 = getCapexData()["monthData"]["data1"]
    res = execute_capex_command(data1, ["CAPEX", "DEC21", "PH333"], "567567")
    print(res)
