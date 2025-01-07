import pandas
import datetime

def not_contains_astrik(text): 
    return "*" not in text 

def get_staff_strength(type="Staff", designation="ALL"):
    if type == "Staff":
        url = "https://docs.google.com/spreadsheets/d/1d18VYLtcfhTkFtd1oszOHW3EQOqReMnchzgtd--FdBA/gviz/tq?tqx=out:csv&sheet=Staff"
    else:
        url = "https://docs.google.com/spreadsheets/d/1d18VYLtcfhTkFtd1oszOHW3EQOqReMnchzgtd--FdBA/gviz/tq?tqx=out:csv&sheet=Officer"
    data = pandas.read_csv(url)
    data['W.E.F.'] = pandas.to_datetime(data['W.E.F.'], format='%d-%m-%Y')
    if type == "Staff":
        strength = data[data["NAME"] != "VACANT"]["DESIG"].value_counts()
    else:
        strength = data[(data["NAME"] != "VACANT") & (data["NAME"].apply(not_contains_astrik))]["Scale"].value_counts()
    msg = f"{type} On Roll is as under:\n"
    if designation == "ALL":
        for desig, count in strength.items():
            msg += f"{desig}: {count}\n"
    else:
        msg += f"{designation}: {strength[designation]}\n"
    msg += "Vacancy position is as under:\n"
    if type == "Staff":
        vacant = data[data["NAME"] == "VACANT"]["DESIG"].value_counts()
    else:
        vacant = data[data["NAME"] == "VACANT"]["Scale"].value_counts()
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
    url = "https://docs.google.com/spreadsheets/d/1d18VYLtcfhTkFtd1oszOHW3EQOqReMnchzgtd--FdBA/gviz/tq?tqx=out:csv&sheet=Staff"
    data = pandas.read_csv(url)
    data['W.E.F.'] = pandas.to_datetime(data['W.E.F.'], format='%d-%m-%Y')
    onroll = data[data["NAME"] != "VACANT"]
    today = datetime.datetime.now()
    onroll["TIME"] = today-onroll["W.E.F."]
    onroll["TIME"] = [time.days/365 for time in onroll["TIME"]]
    msg = "Age-wise breakup of staff is as under:\n"
    onroll = onroll.sort_values(['TIME'], ascending=False)
    due1 = onroll[(onroll["TIME"] > 3) & (onroll["TIME"] < 4)]
    due2 = onroll[(onroll["TIME"] > 4) & (onroll["TIME"] < 5)]
    due3 = onroll[onroll["TIME"] > 5]
    msg += "Staff posted for more than 5 years:\n"
    for index, row in due3.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}/{row['SECTION']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due3['NAME'].count()}\n\n"
    msg += "Staff posted for more than 4 years:\n"
    for index, row in due2.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}/{row['SECTION']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due2['NAME'].count()}\n\n"
    msg += "Staff posted for more than 3 years:\n"
    for index, row in due1.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}/{row['SECTION']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due1['NAME'].count()}\n\n"
    msg += f"Grand Total- {due1['NAME'].count()+ due2['NAME'].count()+ due3['NAME'].count()}"
    return msg

def get_officer_rotation_status(designation="ALL"):
    url = "https://docs.google.com/spreadsheets/d/1d18VYLtcfhTkFtd1oszOHW3EQOqReMnchzgtd--FdBA/gviz/tq?tqx=out:csv&sheet=Officer"
    data = pandas.read_csv(url)
    data['W.E.F.'] = pandas.to_datetime(data['W.E.F.'], format='%d-%m-%Y')
    onroll = data[(data["NAME"] != "VACANT") & (data["NAME"].apply(not_contains_astrik))]
    today = datetime.datetime.now()
    onroll["TIME"] = today-onroll["W.E.F."]
    onroll["TIME"] = [time.days/365 for time in onroll["TIME"]]
    msg = "Age-wise breakup of officers is as under:\n"
    onroll = onroll.sort_values(['TIME'], ascending=False)
    due1 = onroll[(onroll["TIME"] > 3) & (onroll["TIME"] < 4)]
    due2 = onroll[(onroll["TIME"] > 4) & (onroll["TIME"] < 5)]
    due3 = onroll[onroll["TIME"] > 5]
    msg += "Officers posted for more than 5 years:\n"
    for index, row in due3.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due3['NAME'].count()}\n\n"
    msg += "Officers posted for more than 4 years:\n"
    for index, row in due2.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due2['NAME'].count()}\n\n"
    msg += "Officers posted for more than 3 years:\n"
    for index, row in due1.iterrows():
        msg += f"{row['NAME']}, {row['DESIG']}: {round(row['TIME'], 1)} years\n"
    msg += f"Total- {due1['NAME'].count()}\n\n"
    msg += f"Grand Total- {due1['NAME'].count()+ due2['NAME'].count()+ due3['NAME'].count()}"
    return msg

def get_post_codes(post):
    url = "https://docs.google.com/spreadsheets/d/1d18VYLtcfhTkFtd1oszOHW3EQOqReMnchzgtd--FdBA/gviz/tq?tqx=out:csv&sheet=Officer"
    data = pandas.read_csv(url)
    data['W.E.F.'] = pandas.to_datetime(data['W.E.F.'], format='%d-%m-%Y')
    if post == "ALL":
        post_codes = data[data["Post Code"].notna()]
    else:
        post_codes = data[(data["Post Code"].notna()) & (data["Scale"] == post)]
    msg = f"Post codes for {post} posts are as below:\n"
    for index, item in post_codes.iterrows():
        msg += f"{item['DESIG']}: {item['Post Code']}\n"
    return msg

if __name__ == "__main__":
    # data = get_staff_strength(type="Officer", designation="ALL")
    # data = get_post_codes("JAG/SG")
    data = get_officer_rotation_status()
    print(data)