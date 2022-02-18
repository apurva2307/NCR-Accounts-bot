from database import get_owe_data
from helpers import *


def get_data_type_two(title, puData1, puData2, percent, *args):
    showPercent = "%" if percent else ""
    msg = f"{title}\n<b><i>Fig. in thousand</i></b>\n"
    cr = False
    for arg in args:
        if arg == "CR":
            msg = f"{title}\n<b><i>Fig. in crore</i></b>\n"
            cr = True
    for index, value in enumerate(puData1):
        value1 = value if cr == False else value / 1000
        value2 = (
            puData2[index]
            if cr == False
            else puData2[index] / 1000
            if showPercent == ""
            else puData2[index]
        )
        if index == 11:
            msg += f"Total: {value1} ({value2}{showPercent})\n"
        else:
            msg += f"D{index+3}: {value1} ({value2}{showPercent})\n"
    return msg


def showSummary(pu, data2):
    puData = data2[pu]
    msg = "Figures in crores\n"
    for index, val in enumerate(puData):
        if index == 0:
            msg += f"Actuals Full Last Year: {val}"
    return msg
