"""Riot module: official API (developer key from developer.riotgames.com).

What it provides: puuid, LoL match history, play hours (-> likely time
zone), frequent teammates.
Limitation: Valorant endpoints (val-match-v1) require a production key
approved by Riot. With a dev key, the API part is limited to LoL;
Valorant can be handled manually (public stats sites) and documented.
"""
import os
import time
from collections import Counter
from datetime import datetime, timezone

import requests

# Regional routing: "europe" for EUW/EUNE/TR/RU, "americas", "asia"
REGION = os.environ.get("RIOT_REGION", "europe")


class RiotError(Exception):
    pass


def _get(url: str, params: dict | None = None):
    key = os.environ.get("RIOT_API_KEY", "").strip().strip('"').strip("'")
    if not key:
        raise RiotError("Missing RIOT_API_KEY environment variable.")
    for _ in range(3):
        r = requests.get(url, params=params, headers={"X-Riot-Token": key}, timeout=15)
        if r.status_code == 429:  # rate limit
            time.sleep(int(r.headers.get("Retry-After", "2")))
            continue
        if r.status_code in (401, 403):
            raise RiotError(
                f"API key rejected (HTTP {r.status_code}): missing, badly copied or expired key "
                "(dev keys last 24 h). Regenerate it at developer.riotgames.com."
            )
        if r.status_code == 404:
            return None
        if not r.ok:
            raise RiotError(f"HTTP error {r.status_code} from the Riot API.")
        return r.json()
    raise RiotError("Persistent rate limit.")


def get_account(game_name: str, tag_line: str) -> dict | None:
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    return _get(url)


def get_match_ids(puuid: str, count: int = 100) -> list[str]:
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    return _get(url, {"start": 0, "count": min(count, 100)}) or []


def get_match(match_id: str) -> dict | None:
    return _get(f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}")


def analyse(game_name: str, tag_line: str, max_matches: int = 40) -> dict:
    """Analyses activity: play hours (UTC) and recurring teammates."""
    account = get_account(game_name, tag_line)
    if not account:
        return {"found": False}
    puuid = account["puuid"]
    hours, mates = Counter(), Counter()
    for mid in get_match_ids(puuid, max_matches):
        m = get_match(mid)
        if not m:
            continue
        info = m["info"]
        ts = datetime.fromtimestamp(info["gameStartTimestamp"] / 1000, tz=timezone.utc)
        hours[ts.hour] += 1
        me_team = next((p["teamId"] for p in info["participants"] if p["puuid"] == puuid), None)
        for p in info["participants"]:
            if p["puuid"] != puuid and p["teamId"] == me_team:
                name = f'{p.get("riotIdGameName", "?")}#{p.get("riotIdTagline", "?")}'
                mates[name] += 1
    return {
        "found": True,
        "riot_id": f'{account["gameName"]}#{account["tagLine"]}',
        "puuid": puuid,
        "hours_utc": dict(sorted(hours.items())),
        "peak_hours_utc": [h for h, _ in hours.most_common(3)],
        "frequent_teammates": [n for n, c in mates.most_common(10) if c >= 3],
        "matches_analysed": sum(hours.values()),
    }
