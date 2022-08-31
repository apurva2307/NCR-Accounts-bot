import pandas


def get_data(url):
    data = pandas.read_csv(url, skiprows=[8, 11], nrows=145)
    listOfColumns = list(data)
    newCols = {}
    colsMap = [
        "PH",
        "Allocation",
        "CON-Budget",
        "CON-Actuals upto Month",
        "CON-Budget Utilization",
        "OpenLine-Budget",
        "OpenLine-Actuals upto Month",
        "OpenLine-Budget Utilization",
        "NCR-Budget",
        "NCR-Actuals upto Month",
        "NCR-Budget Utilization",
    ]
    for i, val in enumerate(listOfColumns):
        if i <= len(colsMap) - 1:
            newCols[val] = colsMap[i]
        else:
            newCols[val] = "Skip"
    data.rename(columns=newCols, inplace=True)
    data = data[
        [
            "PH",
            "Allocation",
            "CON-Budget",
            "CON-Actuals upto Month",
            "CON-Budget Utilization",
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
        print(prevValue)
        if value != 0:
            prevValue = value
            if (
                "Total" in value
                or "Credit" in value
                or "Net" in value
                or "Source" in value
                or "Suspense" in value
            ):
                pass
            else:
                data.at[index, "PH"] = f"PH{value[:2]}"

        if value == 0:
            if "Total" in prevValue or "Credit" in prevValue or "Net" in prevValue:
                pass
            elif "Source" in prevValue:
                data.at[index, "PH"] = prevValue
            else:
                data.at[index, "PH"] = f"PH{prevValue[:2]}"
    return data


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


url = "https://docs.google.com/spreadsheets/d/1zHlN8IG10LGy0a7W0WCnN1b7sXNqSTDh/gviz/tq?tqx=out:csv&sheet=Capex%20Review%20April-2022"


def get_phdata(df, ph):
    phData = df[df["PH"] == ph]
    result = {}
    for index, val in phData.iterrows():
        rowData = list(val)
        print(rowData)
        result[rowData[1]] = rowData[2:]
    return result


if __name__ == "__main__":
    error = ""
    df = ""
    try:
        df = get_data(url)
        print(df)
    except:
        error = "No data"
        print(error)
    if isinstance(df, pandas.DataFrame):
        df.to_csv("capex.csv", index=False)
        ncrData = get_unit_data(df, "NCR")
        print(ncrData)
        # ph16ncrData = ncrData[ncrData["PH"] == "PH15"]
        # print(ph16ncrData)
        # # print(df[df["PH"] == "1100- New Lines Construction"])
        # # print(df.iloc[70:])
        # print(get_phdata(ncrData, "PH15"))
        # print(ncrData[ncrData["Allocation"] == "Total EBR-IF"])
        for val in ncrData.iterrows():
            print(val)
