import requests
import csv
import time
import os
import random

API_KEY = "YOUR_API_KEY_HERE"
REGION = "na"
PLATFORM = "pc"

INPUT_PLAYERS_FILE = "na_leaderboard_puuids.csv"
OUTPUT_MATCHES_FILE = "matches.csv"

SIZE = 10
MAX_MATCHES_PER_PLAYER = 50  # 50 matches per player
SLEEP_SECONDS = 2.2  # safe for 30 requests per minute

#Program to get 50 matches from each player using the players name and tag

#Load existing matches, used to check for dupes.
existing_match_ids = set()

if os.path.exists(OUTPUT_MATCHES_FILE):
    with open(OUTPUT_MATCHES_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_match_ids.add(row["match_id"])

print(f"Loaded {len(existing_match_ids)} existing matches.")



file_exists = os.path.exists(OUTPUT_MATCHES_FILE)

outfile = open(OUTPUT_MATCHES_FILE, "a", newline='', encoding="utf-8")
writer = csv.writer(outfile)


#Fetches matches from herik's unofficial valorant API, You can swap this with normal valorant API and should work as intended
def fetch_matches(name, tag, start):

    url = f"https://api.henrikdev.xyz/valorant/v4/matches/{REGION}/{PLATFORM}/{name}/{tag}"
    while True:
        response = requests.get(
            url,
            headers={"Authorization": API_KEY},
            params={
                "size": "10",
                "start": start,
                "mode": "competitive"
            }
        )

        if response.status_code == 200:
            remaining = int(response.headers.get("x-ratelimit-remaining", 5))

            sleep_time = SLEEP_SECONDS

            if remaining <= 1:
                sleep_time = 30
            elif remaining <= 3:
                sleep_time = 3
            sleep_time += random.uniform(0.2, 0.5)

            
            time.sleep(sleep_time)  # rate limit safe
            print(f"Loaded {name}, start: {start}, remaining: {remaining}.\n")
            return response.json().get("data", [])


        elif response.status_code == 429:
            retry_after = 20
            print(f"Error 429. Sleeping {retry_after + 1} seconds...")
            time.sleep(retry_after + 1)
            continue
        else:
            print(f"Unexpected error: {response.status_code}\n {response.text}\n")
            return []


def main():
    #opens leaderboard file for reading
    with open(INPUT_PLAYERS_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)

        #reads every player doing a query for their match data
        for player in reader:
            name = player["gameName"]
            tag = player["tagLine"]

            print(f"Fetching for {name}#{tag}.\n")

            for start in range(0, MAX_MATCHES_PER_PLAYER, SIZE):

                matches = fetch_matches(name, tag, start)

                if not matches:
                    break

                #grab data from each match
                for match in matches:

                    match_id = match["metadata"]["match_id"]

                    if match_id in existing_match_ids:
                        continue

                    start_time = match["metadata"]["started_at"]

                    total_head = 0
                    total_body = 0
                    total_leg = 0

                    headshot_percentages = []

                    for p in match["players"]:
                        stats = p["stats"]

                        head = stats.get("headshots", 0)
                        body = stats.get("bodyshots", 0)
                        leg = stats.get("legshots", 0)

                        total = head + body + leg

                        total_head += head
                        total_body += body
                        total_leg += leg

                        if total > 0:
                            headshot_percentages.append(head / total)

                    avg_hs = (
                        sum(headshot_percentages) / len(headshot_percentages)
                        if headshot_percentages else 0
                    )

                    writer.writerow([
                        match_id,
                        start_time,
                        total_head,
                        total_body,
                        total_leg,
                        avg_hs
                    ])

                    existing_match_ids.add(match_id)

            print(f"Finished {name}#{tag}\n")
    #close file being written to.
    outfile.close()
    print("Done.")

if __name__ == "__main__":
    main()