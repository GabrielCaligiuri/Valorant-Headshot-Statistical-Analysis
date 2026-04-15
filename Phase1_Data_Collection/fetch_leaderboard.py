import requests
import time
import csv

API_KEY = "YOUR_API_KEY_HERE"
ACT_ID = "INPUT_CURRENT_ACT_ID_HERE"

REGION = "na"
HEADERS = {"X-Riot-Token": API_KEY}
PLATFORM_URL = "https://na.api.riotgames.com"
OUTPUT_FILE = "na_leaderboard_puuids.csv"

#Program to get leaderboards from Riot's API

#Error handling
def riot_get(url):
    while True:
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            return response

        #rate limit error
        elif response.status_code == 429:
            print(f"Rate limited.")
            print(response.headers["x-ratelimit-remaining"])
            return None

        #Forbidden error (Usually happens after rate limit error)
        elif response.status_code == 403:
            print("403 Forbidden — likely expired API key or temporary block.")
            print(response.text)
            return None

        else:
            print("Unexpected error:", response.status_code)
            print(response.text)
            return None


# FETCH LEADERBOARD
def fetch_leaderboard(act_id):
    puuids = []
    size = 200
    start_index = 0

    while True:
        url = (
            f"{PLATFORM_URL}/val/ranked/v1/leaderboards/by-act/"
            f"{act_id}?size={size}&startIndex={start_index}"
        )

        print(f"Fetching leaderboard page starting at {start_index}...")
        response = riot_get(url)

        if response is None:
            break

        data = response.json()
        players = data.get("players", [])

        if not players:
            break

        for player in players:
            puuids.append({
                "puuid": player["puuid"],
                "gameName": player.get("gameName", ""),
                "tagLine": player.get("tagLine", ""),
                "leaderboardRank": player.get("leaderboardRank", ""),
                "rankedRating": player.get("rankedRating", "")
            })

        print(f"Collected {len(puuids)} players so far...")

        if len(players) < size:
            break

        start_index += size

        # Slow down intentionally to avoid rate limiting error
        time.sleep(1.0)

    return puuids

#Saves to file
def save_to_csv(players):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "puuid",
                "gameName",
                "tagLine",
                "leaderboardRank",
                "rankedRating"
            ]
        )

        writer.writeheader()
        writer.writerows(players)

    print(f"Saved {len(players)} players to {OUTPUT_FILE}")


def main():
    print("Fetching leaderboard players...")
    players = fetch_leaderboard(ACT_ID)

    if players:
        save_to_csv(players)
    else:
        print("No players fetched.")

if __name__ == "__main__":
    main()