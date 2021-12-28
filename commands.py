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
                    result += f"{index+1}. {item}\n"
                broadcast_msg(chat_id, result)
        else :
            broadcast_msg(chat_id, "Nil pending item.")
    elif command[:12] == "/pending add":
        item = command[12:]
        if os.path.isfile("pendingItems.pkl"):
            with open("pendingItems.pkl", "rb") as keyPickle:
                file = pickle.load(keyPickle)
                newList = [*file, item]
                with open("pendingItems.pkl", "wb") as keyPickle:
                    pickle.dump(newList, keyPickle)
                    broadcast_msg(chat_id, "New item added successfully.")
        else :
            newList = [item]
            with open("pendingItems.pkl", "wb") as keyPickle:
                    pickle.dump(newList, keyPickle)
                    broadcast_msg(chat_id, "New item added successfully.")
    elif command[:12] == "/pending del":
        itemNum = command[12:]
        try: itemNum = int(itemNum)
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
                itemToDel = file[itemNum-1]
                file.remove(itemToDel)
                newList = [*file]
                with open("pendingItems.pkl", "wb") as keyPickle:
                    pickle.dump(newList, keyPickle)
                    broadcast_msg(chat_id, f"Item no. {itemNum} deleted successfully.")
            if len(newList) == 0:
                os.remove("pendingItems.pkl")
                return
        else :
            broadcast_msg(chat_id, "No pending item exists for deletion.")
    elif command == "/help":
        help_msg = "<pre>Following are the options:</pre>"
        broadcast_msg(chat_id, help_msg)
    elif (
        command[:5].lower() == "/all "
        and chat_id == 44114772
        and command[5:8].lower() == "img"
    ):
        data = {"type": "image"}
        with open("img.pkl", "wb") as imgFile:
            pickle.dump(data, imgFile)
    elif (
        command[:5].lower() == "/all "
        and chat_id == 44114772
        and command[5:9].lower() == "file"
    ):
        data = {"type": "file"}
        with open("file.pkl", "wb") as imgFile:
            pickle.dump(data, imgFile)
    elif command[:5] == "/all " and chat_id == 44114772:
        msg = command[5:]
        print("HI")
        broadcastToAll(msg)
    else:
        broadcast_msg(chat_id, "No such command exists..")