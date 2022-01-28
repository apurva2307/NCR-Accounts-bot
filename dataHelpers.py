from database import get_owe_data
from helpers import *


def get_data_type_two(title, puData1, puData2, percent):
    showPercent = "%" if percent else ""
    msg = f"{title}\n <b>Fig. in thousand</b>"
    for index, value in enumerate(puData1):
        if index == 11:
            msg += f"Total: {value} ({puData2[index]}{showPercent})\n"
        else:
            msg += f"D{index+3}: {value} ({puData2[index]}{showPercent})\n"
    return msg
