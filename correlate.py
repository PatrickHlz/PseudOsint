"""Correlation: identical avatars (perceptual hash) and first/last name candidates with a score."""
import io
import re
from collections import defaultdict

import imagehash
import requests
from PIL import Image

NAME_RE = re.compile(r"\b([A-ZÉÈ][a-zéèëïîôç]+(?:-[A-ZÉÈ][a-zéèëïîôç]+)?)\s+([A-ZÉÈ][a-zéèëïîôç]+|[A-ZÉÈ]{3,})\b")


def avatar_hash(url: str):
    try:
        img = Image.open(io.BytesIO(requests.get(url, timeout=10).content))
        return imagehash.phash(img)
    except Exception:
        return None


def same_avatars(profiles: list[dict], threshold: int = 6) -> list[tuple[str, str]]:
    """Profile pairs with (nearly) identical avatars: strong evidence that they belong to the same person."""
    hashes = [(p.get("source", "?"), avatar_hash(p["avatar_url"])) for p in profiles if p.get("avatar_url")]
    pairs = []
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            if hashes[i][1] is not None and hashes[j][1] is not None:
                if hashes[i][1] - hashes[j][1] <= threshold:
                    pairs.append((hashes[i][0], hashes[j][0]))
    return pairs


def name_candidates(profiles: list[dict]) -> list[dict]:
    """Extracts "First Last" pairs from text fields; the more a name appears on independent sources,
    the higher the score."""
    seen = defaultdict(set)
    for p in profiles:
        src = p.get("source", "?")
        texts = [p.get(k) or "" for k in ("name", "bio", "title", "description")] + p.get("emails", [])
        for t in texts:
            for m in NAME_RE.finditer(t):
                seen[f"{m.group(1)} {m.group(2)}"].add(src)
    ranked = [{"candidate": n, "sources": sorted(s), "score": len(s)} for n, s in seen.items()]
    return sorted(ranked, key=lambda x: -x["score"])
