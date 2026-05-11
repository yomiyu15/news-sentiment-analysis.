"""Text and publisher normalization helpers for FNSPID-style data."""

from __future__ import annotations

import re


def extract_publisher_domain(publisher: str | None) -> str:
    """
    Normalize publisher labels: if value looks like an email, return the domain
    (e.g. 'analyst@reuters.com' -> 'reuters.com'). Otherwise return stripped text.
    """
    if publisher is None or (isinstance(publisher, float) and str(publisher) == "nan"):
        return ""
    s = str(publisher).strip()
    if not s:
        return ""
    if "@" in s:
        parts = s.rsplit("@", 1)
        if len(parts) == 2 and parts[1]:
            return parts[1].strip().lower()
    return s.lower()


def headline_char_length(headline: str | None) -> int:
    """Return character count for a headline; empty/missing -> 0."""
    if headline is None or (isinstance(headline, float) and str(headline) == "nan"):
        return 0
    return len(str(headline))
