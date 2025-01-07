from database import get_owe_data
from helpers.helpers import *
from datetime import datetime

currentMonth = datetime.now().month
frMonth = currentMonth - 4 if currentMonth > 4 else currentMonth + 8
skip = [
    "PU3",
    "PU7",
    "PU9",
    "PU14",
    "PU15",
    "PU17",
    "PU19",
    "PU20",
    "PU22",
    "PU23",
    "PU24",
    "PU25",
    "PU29",
    "PU36",
    "PU37",
    "PU38",
    "PU40",
    "PU41",
    "PU42",
    "PU43",
    "PU44",
    "PU48",
    "PU51",
    "PU52",
    "PU53",
    "PU72",
    "PU73",
    "PU74",
    "PU75",
    "NONSTAFF",
    "GROSS",
    "CREDIT",
    "NET",
]
dMap = {
    "D3": 0,
    "D4": 1,
    "D5": 2,
    "D6": 3,
    "D7": 4,
    "D8": 5,
    "D9": 6,
    "D10": 7,
    "D11": 8,
    "D12": 9,
    "D13": 10,
    "TOTAL": -1,
}


def highUtilStaff(monthdata, demand, margin):
    result = {}
    for pu, value in monthdata.items():
        if pu == "STAFF":
            break
        if pu in skip:
            continue
        if (
            monthdata[pu]["budgetUtilization"][dMap[demand]]
            > ((frMonth / 12) * 100) + margin
            and monthdata[pu]["toEndActuals"][dMap[demand]] > 5000
        ):
            result[pu] = monthdata[pu]["budgetUtilization"][dMap[demand]]
    return result


def highUtilNonStaff(monthdata, demand, margin):
    result = {}
    for index, pu in enumerate(monthdata.keys()):
        staffIndex = list(monthdata.keys()).index("STAFF")
        if index > staffIndex:
            if pu in skip:
                continue
            if (
                monthdata[pu]["budgetUtilization"][dMap[demand]]
                > ((frMonth / 12) * 100) + margin
                and monthdata[pu]["toEndActuals"][dMap[demand]] > 5000
            ):
                result[pu] = monthdata[pu]["budgetUtilization"][dMap[demand]]
    return result


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


def showSummary(pu, data2, grant):
    puData = data2[pu]
    msg = "Figures in crores\n"
    if pu in ["IRCA", "IRFA", "IRFC", "COACH-C", "STATION-C", "COLONY-C"]:
        for index, val in enumerate(puData):
            if index == 0:
                msg += f"Actuals Full Last Year: {val}\n"
            elif index == 1:
                msg += f"{grant}: {val}\n"
            elif index == 2:
                msg += f"Actuals upto month COPPY: {val}\n"
            elif index == 3:
                msg += f"Actuals upto month: {val}\n"
            elif index == 4:
                msg += f"Variation over COPPY absolute: {val}\n"
            elif index == 5:
                msg += f"Variation over COPPY percentage: {val}%\n"
            elif index == 6:
                msg += f"Budget utilization: {val}%\n"
    else:
        for index, val in enumerate(puData):
            if index == 0:
                msg += f"Actuals Full Last Year: {val}\n"
            elif index == 1:
                msg += f"{grant}: {val}\n"
            elif index == 2:
                msg += f"Actuals upto month COPPY: {val}\n"
            elif index == 4:
                msg += f"Actuals upto month: {val}\n"
            elif index == 7:
                msg += f"Variation over COPPY absolute: {val}\n"
            elif index == 8:
                msg += f"Variation over COPPY percentage: {val}%\n"
            elif index == 9:
                msg += f"Budget utilization: {val}%\n"
    return msg
