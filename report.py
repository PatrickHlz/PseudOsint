"""Markdown report generation (timeline of discoveries, meant to be projected during a demo)."""
from datetime import datetime


def build(data: dict) -> str:
    L = [f"# OSINT Report: {', '.join(data['pseudos'])}", f"_Generated on {datetime.now():%Y-%m-%d %H:%M}_", ""]

    L += ["## 1. Usernames and variants tested", ", ".join(data["variants"]), ""]

    riot = data.get("riot")
    L.append("## 2. Game data (Riot API)")
    if riot and riot.get("found"):
        L += [
            f"- Account: **{riot['riot_id']}** ({riot['matches_analysed']} matches analysed)",
            f"- Most frequent play hours (UTC): {riot['peak_hours_utc']}",
            f"- Recurring teammates: {', '.join(riot['frequent_teammates']) or 'none'}",
        ]
    else:
        L.append("- No data (missing key or account not found).")
    L.append("")

    L.append("## 3. Accounts found on other platforms")
    for a in data["accounts"]:
        L.append(f"- [{a['site']}]({a['url']}) ({a['category']}), username `{a['username']}`")
    L.append("")

    L.append("## 4. Information extracted from profiles")
    for p in data["profiles"]:
        L.append(f"- **{p.get('source')}**: name={p.get('name') or p.get('title')}, bio={p.get('bio') or p.get('description')}")
        for e in p.get("emails", []):
            L.append(f"  - commit e-mail: {e}")
    L.append("")

    L.append("## 5. Correlation")
    L.append(f"- Identical avatars across sources: {data['same_avatars'] or 'none'}")
    L.append("")
    L.append("### First/last name candidates (score = number of independent sources)")
    for c in data["names"][:10]:
        L.append(f"- **{c['candidate']}**: score {c['score']} ({', '.join(c['sources'])})")
    L += ["", "## 6. Prevention tips",
          "- Use a different username on each platform", "- Private profiles / streamer mode",
          "- Do not reuse the same avatar from one site to another", "- Dedicated e-mail address for commits (GitHub noreply)",
          "- Delete old unused accounts"]
    return "\n".join(L)
