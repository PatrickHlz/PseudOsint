"""Generation of username variants (doubled letters, case, leet, suffixes)."""
import itertools

LEET = {"o": "0", "i": "1", "e": "3", "a": "4", "s": "5", "l": "1"}
SUFFIXES = ["", "_", "1", "01", "fr", "_fr", "xx", "yt", "off", "tv"]


def doubled_letters(pseudo: str) -> set[str]:
    """Pseudo -> Pseeudo, Pseudoo... (one doubled letter at a time)."""
    out = set()
    for i, ch in enumerate(pseudo):
        if ch.isalpha():
            out.add(pseudo[:i] + ch + pseudo[i:])
    return out


def removed_letters(pseudo: str) -> set[str]:
    """XeelOosS -> XelOosS (one removed letter at a time)."""
    return {pseudo[:i] + pseudo[i + 1:] for i in range(len(pseudo)) if len(pseudo) > 3}


def leet(pseudo: str) -> set[str]:
    out = set()
    for i, ch in enumerate(pseudo):
        if ch.lower() in LEET:
            out.add(pseudo[:i] + LEET[ch.lower()] + pseudo[i + 1:])
    return out


def generate(*pseudos: str, with_suffixes: bool = False) -> list[str]:
    """Returns the deduplicated (case-insensitive) list of variants."""
    base = set(pseudos)
    variants = set(base)
    for p in base:
        variants |= doubled_letters(p) | removed_letters(p) | leet(p)
        variants |= {p.lower(), p.upper()}
    # The original usernames always come first
    if with_suffixes:
        variants |= {v + s for v, s in itertools.product(list(variants), SUFFIXES)}
    seen, ordered = set(), []
    for p in list(pseudos) + sorted(variants):
        if p.lower() not in seen:
            seen.add(p.lower())
            ordered.append(p)
    return ordered

