import pandas as pd
from datetime import datetime
import pytz


CSV_FILE = "matches.csv"
OUTPUT_FILE = "cleanData.csv"
TIMEZONE = "US/Mountain"   # Change if needed (US/Pacific, etc.)


#Program to clean the data formatting to make it easy to use to create histograms and analyze.

def compute_stats(data):
    total_shots = data["total_headshots"] + data["total_bodyshots"] + data["total_legshots"]    
    total_head = data["total_headshots"]
    #Weighted HS compares hs% match averages based on # of shots made in the game
    data["weighted_hs"] = total_head / total_shots
    #unweighted treats every game the same no matter the amount of shots fired.
    data["unweighted_hs"] = data["average_headshot_percentage"]
    
    return data

def main():
    #open file
    data = pd.read_csv(CSV_FILE)

    #Change formatting of datetime
    data["start_time"] = pd.to_datetime(data["start_time"], utc=True, format="mixed")
    #change timezone
    local_tz = pytz.timezone(TIMEZONE)
    data["local_time"] = data["start_time"].dt.tz_convert(local_tz)

    # 0=Monday, 6=Sunday
    data["weekday_number"] = data["local_time"].dt.weekday

    #Splits population into weekdays and weekends
    data["Time"] = data["weekday_number"].apply(
        lambda x: "Weekday" if x <= 3 else "Weekend"
    )

    data = compute_stats(data)
    clean_data = data[[
        "Time",
        "weighted_hs",
        "unweighted_hs"
    ]]

    clean_data.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    main()
