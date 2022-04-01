import pandas as pd

url = f"https://docs.google.com/spreadsheets/d/1kXBrVy9mREA1ydLnBrWOxTl0mtfEaZRXi8Q_-IZGYfg/gviz/tq?tqx=out:csv&sheet=Capex"


def get_data(month):
    first = month[0].upper()
    rest = month[1:3].lower()
    month = f"{first}{rest}-{month[3:5]}"
    print(month)
    data = ""
    error = ""
    try:
        data = pd.read_csv(f"{url}{month}", skiprows=[8, 11], nrows=97)
        listOfColumns = list(data)
        newCols = {}
        colsMap = [
            "PH",
            "Allocation",
            "NCRPU-Budget",
            "NCRPU-Actuals upto Month",
            "NCRPU-Budget Utilization",
            "Skip",
            "OpenLine-Budget",
            "OpenLine-Actuals upto Month",
            "OpenLine-Budget Utilization",
            "Skip",
            "NCR-Budget",
            "NCR-Actuals upto Month",
            "NCR-Budget Utilization",
        ]
        for i, val in enumerate(listOfColumns):
            newCols[val] = colsMap[i]
        data.rename(columns=newCols, inplace=True)
        data = data[
            [
                "PH",
                "Allocation",
                "NCRPU-Budget",
                "NCRPU-Actuals upto Month",
                "NCRPU-Budget Utilization",
                "OpenLine-Budget",
                "OpenLine-Actuals upto Month",
                "OpenLine-Budget Utilization",
                "NCR-Budget",
                "NCR-Actuals upto Month",
                "NCR-Budget Utilization",
            ]
        ]
        data = data.fillna(0)
        for index, value in data["PH"].items():
            if value != 0:
                prevValue = value
                if value.startswith("Total"):
                    pass
                else:
                    data.at[index, "PH"] = f"PH{value[:2]}"
            if value == 0:
                if prevValue.startswith("Total"):
                    data.at[index, "PH"] = prevValue
                else:
                    data.at[index, "PH"] = f"PH{prevValue[:2]}"
    except:
        error = "No data found."
    return data, error


def get_unit_data(df, unit):
    unitData = df[
        [
            "PH",
            "Allocation",
            f"{unit}-Budget",
            f"{unit}-Actuals upto Month",
            f"{unit}-Budget Utilization",
        ]
    ]
    return unitData


def get_phdata(df, ph):
    phData = df[df["PH"] == ph]
    result = {}
    result[ph] = {}
    for index, val in phData.iterrows():
        rowData = list(val)
        result[ph][rowData[1]] = rowData[2:]
    return result


if __name__ == "__main__":
    print(get_data("Jan22"))
