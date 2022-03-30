from database import update_user_role, update_user_info, delete_single_user
from helpers import broadcast_msg


def execute_admin_command(cmd, chat_id):
    command = cmd.lower()
    if command[:11] == "updaterole ":
        cmds = command[11:].split(":")
        chatId = cmds[0].strip()
        role = cmds[1].strip()
        roles = ["admin", "user", "banned"]
        if role in roles:
            res = update_user_role(chatId, role)
            broadcast_msg(chat_id, res)
            return "executed"
        else:
            broadcast_msg(chat_id, "Kindly provide valid role.")
            return "executed"
    elif command[:8] == "deluser ":
        res = delete_single_user(command[8:].strip())
        broadcast_msg(chat_id, res)
        return "executed"
    elif command[:11] == "updateinfo ":
        cmds = cmd[11:].split(":")
        chatId = cmds[0].strip()
        infos = cmds[1].strip().split(",")
        otherinfo = {}
        for info in infos:
            otherinfo[info.strip().split("-")[0]] = info.strip().split("-")[1]
        res = update_user_info(chatId, otherinfo)
        broadcast_msg(chat_id, res)
        return "executed"
    else:
        return "No"
