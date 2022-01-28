from database import get_owe_data
from helpers import *


def get_data_type_two(title, puData1, puData2, percent):
    showPercent = "%" if percent else ""
    msg = ""
    for index, value in enumerate(puData1):
        if index == 0:
            msg += f"{title}\nD{index+3}: {value} thousand ({puData2[index]}{showPercent})\n"
        elif index == 11:
            msg += f"Total: {value} thousand ({puData2[index]}{showPercent})\n"
        else:
            msg += f"D{index+3}: {value} thousand ({puData2[index]}{showPercent})\n"
    return msg
