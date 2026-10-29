"""CLI: python main.py --pseudo ... --pseudo ... --riot-id "...#TAG" -o report.md"""
import argparse
from concurrent.futures import ThreadPoolExecutor

import correlate
import enumerate_usernames as enum
import profiles
import report
import riot
import variants


def main():
    ap = argparse.ArgumentParser(description="Educational OSINT pipeline starting from a username.")
    ap.add_argument("--pseudo", action="append", required=True, help="starting username (repeatable)")
    ap.add_argument("--riot-id", help='Full Riot ID "Name#TAG" for the LoL API')
    ap.add_argument("--suffixes", action="store_true", help="add suffixes to the variants (slower)")
    ap.add_argument("--sherlock", action="store_true", help="also use Sherlock (original usernames only)")
    ap.add_argument("--no-variants", action="store_true", help="only test the exact usernames (much faster)")
    ap.add_argument("--categories", help="limit the sites tested, e.g.: gaming,social,coding")
    ap.add_argument("--workers", type=int, default=60, help="parallel requests (default 60)")
    ap.add_argument("--timeout", type=float, default=6, help="max delay per site in seconds (default 6)")
    ap.add_argument("-o", "--output", default="report.md")
    args = ap.parse_args()

    if args.no_variants:
        names = list(dict.fromkeys(args.pseudo))
        print(f"[1/5] {len(names)} exact username(s), no variants")
    else:
        names = variants.generate(*args.pseudo, with_suffixes=args.suffixes)
        print(f"[1/5] {len(names)} variants generated")

    riot_data = None
    if args.riot_id:
        try:
            game, tag = args.riot_id.split("#", 1)
            riot_data = riot.analyse(game, tag)
            print(f"[2/5] Riot: {riot_data.get('riot_id', 'not found')}")
        except riot.RiotError as e:
            print(f"[2/5] Riot skipped: {e}")

    cats = {c.strip().lower() for c in args.categories.split(",")} if args.categories else None
    print("[3/5] Searching for accounts on websites...")
    accounts = enum.enumerate_many(names, cats, args.workers, args.timeout)
    if args.sherlock:
        for n in dict.fromkeys(args.pseudo):
            accounts += [{"site": "sherlock", "category": "", "username": n, "url": u} for u in enum.run_sherlock(n)]
    print(f"[3/5] {len(accounts)} accounts found")

    def fetch_profile(a):
        if a["site"].lower() == "github":
            p = profiles.github_profile(a["username"])
        else:
            p = profiles.generic_profile(a["url"])
        if p:
            p["source"] = a["url"]
        return p

    with ThreadPoolExecutor(max_workers=10) as ex:
        profs = [p for p in ex.map(fetch_profile, accounts) if p]
    print(f"[4/5] {len(profs)} profiles analysed")

    data = {
        "pseudos": args.pseudo, "variants": names, "riot": riot_data, "accounts": accounts,
        "profiles": profs, "same_avatars": correlate.same_avatars(profs),
        "names": correlate.name_candidates(profs),
    }
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report.build(data))
    print(f"[5/5] Report written to {args.output}")


if __name__ == "__main__":
    main()
