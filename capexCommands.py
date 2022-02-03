from helpers import broadcast_msg


def execute_capex_command(data1, cmd, chat_id):
    if len(cmd) == 2:
        totalData = data1["TOTAL"]
        msg = ""
        for key, value in totalData:
            actuals = value["ncr"][-2]
            budUtil = value["ncr"][-1]
            msg = f"for {key}\nactuals = {actuals}, util = {budUtil}"
        broadcast_msg(chat_id, msg)
