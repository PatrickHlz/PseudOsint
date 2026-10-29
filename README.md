# Educational OSINT Project: From a Username to an Identity

**An OSINT tool for combating extreme toxicity in online gaming.**

## Pipeline

1. `variants.py`: Generates username variants (doubled letters, capitalization, leetspeak).
2. `riot.py`: Retrieves Riot Games data, such as PUUID, playtime, and teammates, when API access is configured.
3. `enumerate_usernames.py`: Searches for usernames across hundreds of websites using the WhatsMyName dataset (custom implementation), with optional Sherlock integration.
4. `profiles.py`: Extracts publicly available profile information, including bios, names, avatars, and GitHub commit email addresses.
5. `correlate.py`: Identifies profiles with identical or similar avatars using perceptual hashing and generates scored first-name/last-name candidates.
6. `report.py`: Generates a Markdown report.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

### Riot API Configuration (Optional)

A Riot API key is **optional**. The tool can perform its main username searches and profile correlations without one.

If you want to enable Riot-specific analysis, configure your API key and region:

```bash
export RIOT_API_KEY="RGAPI-xxxxxxxx"
export RIOT_REGION="europe"
```

On Windows PowerShell:

```powershell
$env:RIOT_API_KEY="RGAPI-xxxxxxxx"
$env:RIOT_REGION="europe"
```

Replace the example key with your own valid Riot API key.

Without a Riot API key, Riot-specific information, such as account identifiers and game-related data, may be unavailable. This does **not significantly affect the tool's core functionality**, including username enumeration across websites and profile correlation.

API access, available data, and rate limits depend on Riot Games' current API policies and the type of key being used.

## Usage

```bash
python main.py --pseudo XelOosS --pseudo XeelOosS --riot-id "XelOosS#TAG" --sherlock -o report.md
```

The `--riot-id` argument is optional if you do not need Riot-specific analysis. The `--sherlock` argument is also optional.

Example without Riot-specific analysis:

```bash
python main.py --pseudo XelOosS --pseudo XeelOosS --sherlock -o report.md
```

## Acknowledged Limitations

- Valorant-specific API access may require an appropriate production API key. The Valorant portion may therefore need to be handled manually.
- A real name can only be discovered if it is exposed in publicly accessible information.
- False positives are possible. Every correlation must be manually verified.
- Public usernames, matching avatars, and similar names do not conclusively establish that two accounts belong to the same person.
- Results depend on the availability, accuracy, and accessibility of third-party websites and APIs.

## Legal Notice and Ethical Use Policy

### Purpose and Scope

This project is an educational OSINT tool intended to support online safety and help document severe cases of toxic behavior, harassment, or threats in online gaming.

It may be used to preserve relevant evidence and support reports to the appropriate gaming platforms or competent authorities.

**Toxic behavior does not justify retaliation, doxxing, intimidation, or harassment.**

### Legal Considerations

OSINT (Open-Source Intelligence) is not inherently illegal. However, collecting, combining, using, or disclosing information about another person may violate applicable laws, privacy rights, data protection rules, or platform terms, depending on the circumstances and jurisdiction.

In France, for example:

- **Cyberharassment:** Repeated online harassment may constitute a criminal offense under Article 222-33-2-2 of the French Criminal Code.
- **Doxxing:** Under Article 223-1-1 of the French Criminal Code, certain disclosures of personal information that expose an identifiable person or their family to a direct risk of harm may constitute a criminal offense.
- **Threats and intimidation:** Depending on their nature and circumstances, threats and intimidating conduct may constitute separate criminal offenses.

These examples are provided for informational purposes only. The applicable law and potential penalties depend on the facts of each case.

Official references:

- [French Criminal Code, Article 223-1-1](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049312762)
- [French public service guidance on cyberharassment](https://www.service-public.gouv.fr/particuliers/vosdroits/F32239)

### Prohibited Uses

This tool must not be used to:

- Expose or publish someone's home address, private contact details, or other sensitive personal information for malicious purposes.
- Dox, threaten, intimidate, blackmail, stalk, or harass another person.
- Organize retaliation campaigns against toxic players.
- Publish investigation results to shame, punish, or endanger an individual.
- Access private accounts, bypass access controls, or obtain restricted information without authorization.

**Information being publicly accessible does not automatically make every form of collection, combination, or redistribution lawful.**

### Recommended Procedure in Cases of Extreme Toxicity

If you encounter severe toxicity, targeted harassment, or credible threats in an online game:

1. Preserve relevant evidence, such as screenshots, message logs, usernames, timestamps, and match identifiers.
2. Report the behavior through the game's official reporting system.
3. Block or mute the offending player and avoid escalating the confrontation.
4. If the behavior may constitute a criminal offense, consider contacting the appropriate authorities.
5. Use this tool only for legitimate and lawful purposes. Do not publish personal information or use the results to retaliate.

In France, suspected illegal online content may be reported through the appropriate official channels, including [PHAROS](https://www.internet-signalement.gouv.fr/) where applicable. In an emergency or when someone faces an immediate threat, contact the appropriate emergency services.

### Responsible Use and Disclaimer

This software is provided for educational, research, and legitimate online-safety purposes only. Users are responsible for ensuring that their use of the software complies with applicable laws, privacy obligations, and third-party platform terms.

The tool may produce inaccurate results, false positives, or misleading correlations. A matching username, avatar, or name is not proof of identity or wrongdoing.

The developers do not encourage illegal surveillance, doxxing, retaliation, or harassment. This notice is not legal advice and does not guarantee that any particular use of the software is lawful.

**The goal is to document abuse and seek appropriate remedies, not to become the abuser.**
