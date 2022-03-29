from database import update_user_role, update_user_info
from helpers import broadcast_admin


def execute_admin_command(cmd, chat_id):
    command = cmd.lower()
    if command[:11] == "updaterole ":
        cmds = command[11:].split(":")
        chatId = cmds[0].strip()
        role = cmds[1].strip()
        roles = ["admin", "user", "banned"]
        if role in roles:
            res = update_user_role(chatId, role)
            broadcast_admin(res)
        else:
            broadcast_admin("Kindly provide valid role.")
        return "!", 200

    elif command[:11] == "updateinfo ":
        cmds = cmd[11:].split(":")
        chatId = cmds[0].strip()
        infos = cmds[1].strip().split(",")
        otherinfo = {}
        for info in infos:
            otherinfo[info.strip().split("-")[0]] = info.strip().split("-")[1]
        res = update_user_info(chatId, otherinfo)
        broadcast_admin(res)
        return "!", 200
