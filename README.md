# Educational OSINT Project: From a Username to an Identity

Anti-toxicity OSINT tool for online gaming.

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

## Legal Notice, Ethical Use & Anti-Harassment Policy

### Purpose and Scope

This project is an educational OSINT tool designed to support online safety, document severe cases of toxic behavior, and help users identify publicly available information associated with their own usernames.

It may be used to document extreme cases of online harassment, threats, or abusive behavior for the purpose of reporting them to the relevant platform or competent authorities.

**Toxic behavior does not justify retaliation, doxxing, intimidation, or harassment.**

### Legal Considerations

OSINT (Open-Source Intelligence) is not inherently illegal. However, collecting, correlating, using, or disclosing information about another person may violate applicable laws, privacy rights, data protection rules, or platform terms, depending on the circumstances and jurisdiction.

In France, for example:

- **Cyberharassment:** Repeated online harassment may constitute a criminal offense under Article 222-33-2-2 of the French Criminal Code.
- **Doxxing:** Under Article 223-1-1 of the French Criminal Code, disclosing or transmitting information about a person's private, family, or professional life that can identify or locate them, with the intent of exposing them or their family to a direct risk of harm, may be punishable by up to three years of imprisonment and a €45,000 fine.
- **Threats and intimidation:** Depending on their nature and circumstances, threats and other intimidating conduct may constitute separate criminal offenses.

These examples are provided for informational purposes only. The applicable law and potential penalties depend on the specific facts of each case.

Official references:
- French Criminal Code, Article 223-1-1: https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049312762
- French public service guidance on cyberharassment: https://www.service-public.gouv.fr/particuliers/vosdroits/F32239

### Strictly Prohibited Uses

Users of this project must not use it to:

- Identify, expose, or publish someone's real identity, home address, phone number, private email address, or other sensitive personal information without a lawful basis.
- Dox, threaten, intimidate, blackmail, stalk, or harass another person.
- Retaliate against toxic players by organizing harassment campaigns or encouraging others to target them.
- Publish investigation results to shame, punish, or endanger an individual.
- Circumvent access controls or access private accounts, restricted information, or systems without authorization.

Public availability does not automatically make information lawful to collect, combine, or redistribute.

### Recommended Procedure in Cases of Extreme Toxicity

If you encounter severe toxicity, targeted harassment, or credible threats in an online game:

1. Preserve relevant evidence, such as screenshots, message logs, usernames, timestamps, and match identifiers.
2. Report the behavior through the game's official reporting system.
3. Block or mute the offending player and avoid escalating the confrontation.
4. If the behavior may constitute a criminal offense, consider reporting it to the appropriate authorities.
5. Use this tool only where you have a legitimate and lawful purpose, and do not publish personal information or use the results to retaliate.

In France, suspected illegal online content can be reported through the appropriate official channels, including PHAROS where applicable. In an emergency or when someone faces an immediate threat, contact the appropriate emergency services.

### Responsible Use and Disclaimer

This software is provided for educational, research, and legitimate online-safety purposes only. Users are solely responsible for ensuring that their use of the software complies with applicable laws, privacy obligations, and third-party platform terms.

The tool may produce inaccurate results, false positives, or misleading correlations. A matching username, avatar, or name is not proof of identity or wrongdoing.

The developers do not encourage illegal surveillance, doxxing, retaliation, or harassment. This notice is not legal advice and does not guarantee that any particular use of the software is lawful.

**The goal is to document abuse and seek appropriate remedies—not to become the abuser.**
