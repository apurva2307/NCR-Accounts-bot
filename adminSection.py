import pandas
import datetime

url = "https://docs.google.com/spreadsheets/d/1d18VYLtcfhTkFtd1oszOHW3EQOqReMnchzgtd--FdBA/gviz/tq?tqx=out:csv&sheet=Staff"
data = pandas.read_csv(url)
data['W.E.F.'] = pandas.to_datetime(data['W.E.F.'], format='%d-%m-%Y')

def get_staff_strength(designation="ALL"):
    strength = data[data["NAME"] != "VACANT"]["DESIG"].value_counts()
    msg = "Staff On Roll is as under:\n"
    if designation == "ALL":
        for desig, count in strength.items():
            msg += f"{desig}: {count}\n"
    else:
        msg += f"{designation}: {strength[designation]}\n"
    msg += "Vacancy position is as under:\n"
    vacant = data[data["NAME"] == "VACANT"]["DESIG"].value_counts()
    if designation == "ALL":
        for desig, count in vacant.items():
            msg += f"{desig}: {count}\n"
    else:
        try:
            msg += f"{designation}: {vacant[designation]}"
        except:
            msg += f"{designation}: No vacancy for this post."
    return msg

def get_staff_rotation_status(designation="ALL"):
    onroll = data[data["NAME"] != "VACANT"]
    today = datetime.datetime.now()
    onroll["TIME"] = today-onroll["W.E.F."]
    onroll["TIME"] = [time.days/365 for time in onroll["TIME"]]
    msg = "Age-wise breakup of staff is as under:\n"
    onroll = onroll.sort_values(['TIME'], ascending=False)
    due1 = onroll[(onroll["TIME"] > 3) & (onroll["TIME"] < 4)]
    due2 = onroll[(onroll["TIME"] > 4) & (onroll["TIME"] < 5)]
    due3 = onroll[onroll["TIME"] > 5]
    for index, row in due3.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}/{row['SECTION']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due3['NAME'].count()}\n\n"
    for index, row in due2.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}/{row['SECTION']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due2['NAME'].count()}\n\n"
    for index, row in due1.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}/{row['SECTION']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due1['NAME'].count()}\n\n"
    msg += f"Grand Total- {due1['NAME'].count()+ due2['NAME'].count()+ due3['NAME'].count()}"
    return msg