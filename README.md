# Educational OSINT Project: From a Username to an Identity

Demonstration and prevention tool (public talk). **To be used only on your own
username or with the written consent of the person concerned.**

## Pipeline

1. `variants.py`: username variants (doubled letters, case, leet)
2. `riot.py`: Riot API (puuid, play hours, teammates)
3. `enumerate_usernames.py`: searches the username on hundreds of websites (WhatsMyName dataset, in-house implementation) + optional Sherlock
4. `profiles.py`: extraction of bio / name / avatar / commit e-mails (GitHub)
5. `correlate.py`: identical avatars (perceptual hash) + first/last name candidates with a score
6. `report.py`: Markdown report

## Installation

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export RIOT_API_KEY="RGAPI-xxxxxxxx"   # dev key, valid for 24 h
export RIOT_REGION="europe"
```

## Usage

```
python main.py --pseudo XelOosS --pseudo XeelOosS --riot-id "XelOosS#TAG" --sherlock -o report.md
```

## Acknowledged limitations

- The Valorant API requires a production key: the Valorant part is handled manually.
- A name is only found if it is actually exposed on a public account.
- False positives are possible: every correlation must be verified by hand.
