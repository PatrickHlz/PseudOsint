"""Extraction of information from the profiles found (GitHub first)."""
import re

import requests

HEADERS = {"User-Agent": "student-osint-project"}


def github_profile(username: str) -> dict | None:
    """Public GitHub API: display name, bio, avatar, and commit e-mail addresses."""
    r = requests.get(f"https://api.github.com/users/{username}", headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return None
    d = r.json()
    profile = {
        "source": "github",
        "login": d["login"],
        "name": d.get("name"),
        "bio": d.get("bio"),
        "company": d.get("company"),
        "location": d.get("location"),
        "blog": d.get("blog"),
        "avatar_url": d.get("avatar_url"),
        "emails": github_commit_emails(username),
    }
    return profile


def github_commit_emails(username: str) -> list[str]:
    """Public events sometimes contain the e-mail and author name of commits."""
    r = requests.get(f"https://api.github.com/users/{username}/events/public", headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return []
    found = set()
    for ev in r.json():
        for c in ev.get("payload", {}).get("commits", []):
            author = c.get("author", {})
            email = author.get("email", "")
            if email and "noreply" not in email:
                found.add(f'{author.get("name", "?")} <{email}>')
    return sorted(found)


def generic_profile(url: str) -> dict:
    """Basic retrieval of a public page: title, description, avatar (og: tags)."""
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
    except requests.RequestException:
        return {"source": url}

    def og(prop: str):
        m = re.search(rf'<meta[^>]+property=["\']og:{prop}["\'][^>]+content=["\']([^"\']+)', html)
        return m.group(1) if m else None

    return {"source": url, "title": og("title"), "description": og("description"), "avatar_url": og("image")}
