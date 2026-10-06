"""Seeded prose for held-out attacks.

Detectors must fail because the text is not the approved source,
not because they contain a stored attack sentence.
"""

from __future__ import annotations

import random

_SYLLABLES = (
    "ba", "be", "bi", "bo", "bu", "da", "de", "di", "do", "du",
    "fa", "fe", "fi", "fo", "fu", "la", "le", "li", "lo", "lu",
    "ma", "me", "mi", "mo", "mu", "na", "ne", "ni", "no", "nu",
    "pa", "pe", "pi", "po", "pu", "ra", "re", "ri", "ro", "ru",
    "sa", "se", "si", "so", "su", "ta", "te", "ti", "to", "tu",
)


def prose(seed: int, label: str, words: int = 6) -> str:
    rng = random.Random("%s:%s" % (seed, label))
    tokens = []
    for _ in range(words):
        tokens.append(rng.choice(_SYLLABLES) + rng.choice(_SYLLABLES))
    return " ".join(tokens)


def token(seed: int, label: str) -> str:
    return prose(seed, label, words=1)
