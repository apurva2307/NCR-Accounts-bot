from helpers import *
import os


def is_command(txt):
    return txt[0] == "/"


def execute_command(command, chat_id):
    command = command.lower()
    if command == "/pending":
        if os.path.isfile("pendingItems.pkl"):
            with open("pendingItems.pkl", "rb") as keyPickle:
                file = pickle.load(keyPickle)
                result = ""
                for index, item in enumerate(file):
                    result += f"{index+1}. {item['item']}\n"
                broadcast_msg(chat_id, result)
        else:
            broadcast_msg(chat_id, "Nil pending item.")
    elif command[:13] == "/pending add ":
        item = command[13:]
        if os.path.isfile("pendingItems.pkl"):
            with open("pendingItems.pkl", "rb") as keyPickle:
                file = pickle.load(keyPickle)
                newList = [*file, {"item": item, "chat_id": chat_id}]
                with open("pendingItems.pkl", "wb") as keyPickle:
                    pickle.dump(newList, keyPickle)
                    broadcast_msg(chat_id, "New item added successfully.")
        else:
            newList = [{"item": item, "chat_id": chat_id}]
            with open("pendingItems.pkl", "wb") as keyPickle:
                pickle.dump(newList, keyPickle)
                broadcast_msg(chat_id, "New item added successfully.")
    elif command[:13] == "/pending del ":
        itemNum = command[13:]
        try:
            itemNum = int(itemNum)
        except:
            broadcast_msg(chat_id, "Kindly enter integer number only.")
            return
        if os.path.isfile("pendingItems.pkl"):
            newList = []
            with open("pendingItems.pkl", "rb") as keyPickle:
                file = pickle.load(keyPickle)
                if itemNum < 1 or itemNum > len(file):
                    broadcast_msg(chat_id, "Kindly enter valid pending item number.")
                    return
                if file[itemNum - 1]["chat_id"] == chat_id:
                    del file[itemNum - 1 : itemNum]
                else:
                    broadcast_msg(
                        chat_id,
                        f"Item no. {itemNum} has not been created by you. Kindly enter valid item no. only.",
                    )
                    return
                newList = [*file]
                with open("pendingItems.pkl", "wb") as keyPickle:
                    pickle.dump(newList, keyPickle)
                    broadcast_msg(chat_id, f"Item no. {itemNum} deleted successfully.")
            if len(newList) == 0:
                os.remove("pendingItems.pkl")
                return
        else:
            broadcast_msg(chat_id, "No pending item exists for deletion.")
    elif command == "/help":
        help_msg = "Following are the options:\n"
        item1 = "1. /pending add item_description - to add an item to pending list\n2. /pending del item_number - to delete an item from pending list\n"
        help_msg += item1
        broadcast_msg(chat_id, help_msg)
    elif command[:5] == "/all " and chat_id == 44114772 and command[5:8] == "img":
        data = {"type": "image"}
        with open("img.pkl", "wb") as imgFile:
            pickle.dump(data, imgFile)
    elif command[:5] == "/all " and chat_id == 44114772 and command[5:9] == "file":
        data = {"type": "file"}
        with open("file.pkl", "wb") as imgFile:
            pickle.dump(data, imgFile)
    elif command == "/get_owe_pu":
        if os.path.isfile("owe_pu.pkl"):
            with open("owe_pu.pkl", "rb") as keyPickle:
                file = pickle.load(keyPickle)
                broadcast_items(chat_id, file["owe_pu_file_id"], "Document")
            return
        resp = sendFile(chat_id, "excel", "files\OWE_Nov_21.xlsx", "OWE_Nov_21.xlsx")
        file_id = json.loads(resp)["result"]["document"]["file_id"]
        data = {"owe_pu_file_id": file_id}
        with open("owe_pu.pkl", "wb") as file:
            pickle.dump(data, file)

    elif command[:5] == "/all " and chat_id == 44114772:
        msg = command[5:]
        broadcastToAll(msg)
    else:
        broadcast_msg(chat_id, "No such command exists..")
