"""Username enumeration: our own implementation based on WhatsMyName.

The dataset (wmn-data.json) describes, for each website: the URL to test
({account} = username), the expected HTTP status code if the account exists (e_code) and
a string present on the page (e_string), as well as the corresponding values if
the account does not exist (m_code / m_string).

Source: https://github.com/WebBreacher/WhatsMyName
"""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

WMN_URL = "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
WMN_FILE = "wmn-data.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (student OSINT project - awareness)"}


def load_sites(refresh: bool = False) -> list[dict]:
    if refresh or not os.path.exists(WMN_FILE):
        r = requests.get(WMN_URL, timeout=30)
        r.raise_for_status()
        with open(WMN_FILE, "w", encoding="utf-8") as f:
            f.write(r.text)
    with open(WMN_FILE, encoding="utf-8") as f:
        return json.load(f)["sites"]


def check_site(site: dict, username: str, timeout: float = 10) -> dict | None:
    uri = site.get("uri_check", "").replace("{account}", username)
    if not uri:
        return None
    try:
        r = requests.get(uri, headers=HEADERS, timeout=timeout, allow_redirects=False)
    except requests.RequestException:
        return None
    exists = (
        r.status_code == site.get("e_code")
        and site.get("e_string", "") in r.text
        and (not site.get("m_string") or site["m_string"] not in r.text)
    )
    if not exists:
        return None
    return {
        "site": site["name"],
        "category": site.get("cat", ""),
        "username": username,
        "url": site.get("uri_pretty", uri).replace("{account}", username),
    }


def enumerate_username(username: str, categories: set[str] | None = None, workers: int = 30) -> list[dict]:
    return enumerate_many([username], categories, workers, progress=False)


def enumerate_many(usernames: list[str], categories: set[str] | None = None,
                   workers: int = 60, timeout: float = 6, progress: bool = True) -> list[dict]:
    """Tests all (site, username) pairs in a SINGLE thread pool: much faster
    than processing usernames one by one. NSFW categories are always excluded."""
    sites = [s for s in load_sites() if "nsfw" not in s.get("cat", "").lower()]
    if categories:
        sites = [s for s in sites if s.get("cat", "").lower() in categories]
    jobs = [(s, u) for u in usernames for s in sites]
    results, done = [], 0
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(check_site, s, u, timeout) for s, u in jobs]
        for f in as_completed(futures):
            done += 1
            r = f.result()
            if r:
                results.append(r)
            if progress and done % 200 == 0:
                print(f"\r      {done}/{len(jobs)} tests, {len(results)} accounts found", end="", flush=True)
    if progress:
        print(f"\r      {len(jobs)}/{len(jobs)} tests, {len(results)} accounts found")
    return results


def run_sherlock(username: str) -> list[str]:
    """Additional component: Sherlock (pip install sherlock-project) running as a subprocess."""
    import shutil
    import subprocess

    if not shutil.which("sherlock"):
        return []
    out = subprocess.run(
        ["sherlock", username, "--print-found", "--timeout", "10", "--no-color"],
        capture_output=True, text=True, timeout=300,
    ).stdout
    return [l.split(": ", 1)[1].strip() for l in out.splitlines() if l.startswith("[+]") and ": " in l]
