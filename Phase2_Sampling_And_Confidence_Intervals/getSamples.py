import random as rd
import pandas as pd

CSV_FILE = "cleanData.csv"

def main():
    data = pd.read_csv(CSV_FILE)

    column = "Time"

    weekdayData = data[data[column] == "Weekday"]
    weekendData = data[data[column] == "Weekend"]

    sampleSizes = [10, 12, 15]
    weekdayList = []
    weekendList = []
    for n in sampleSizes:
        
        weekdaySelection = rd.sample(range(len(weekdayData)), n)
        weekendSelection = rd.sample(range(len(weekendData)), n)
        
        weekdaySelections = weekdayData.iloc[weekdaySelection].copy()
        weekdaySelections["sample_size"] = n
        weekdaySelections = weekdaySelections.drop(columns=["weighted_hs"])


        weekendSelections = weekendData.iloc[weekendSelection].copy()
        weekendSelections["sample_size"] = n
        weekendSelections = weekendSelections.drop(columns=["weighted_hs"])

        weekdayList.append(weekdaySelections)
        weekendList.append(weekendSelections)

    finalSamples = pd.concat(weekdayList + weekendList)
    finalSamples.to_csv("Phase4_Samples.csv", index=False)

if __name__ == "__main__":
    main()









