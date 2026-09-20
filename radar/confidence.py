"""Discovery confidence helpers (migrated from find_arxiv_candidates)."""

from __future__ import annotations

import re

WORLD_RE = re.compile(
    r"\bworld(?:[-\s]+(?:action|foundation))?[-\s]+model(s|ing|ling)?\b",
    re.IGNORECASE,
)
OVERVIEW_RE = re.compile(
    r"\b(survey|review|roadmap|taxonomy|definition|framework|position|critique|"
    r"future directions?|challenges?|benchmarks?|opportunit(?:y|ies))\b",
    re.IGNORECASE,
)
TITLE_OVERVIEW_RE = re.compile(
    r"\b(survey|review|roadmap|taxonomy|definition|framework|position|perspective|"
    r"critique|future directions?|challenges?|benchmark)\b",
    re.IGNORECASE,
)


def assess_discovery_confidence(title: str, summary: str) -> tuple[str, list[str]]:
    """Rate search evidence only; inclusion still requires manual primary-source review."""
    world_in_title = bool(WORLD_RE.search(title))
    overview_in_title = bool(TITLE_OVERVIEW_RE.search(title))
    overview_in_summary = bool(OVERVIEW_RE.search(summary))

    evidence: list[str] = []
    if world_in_title:
        evidence.append("world-model phrase appears in title")
    if overview_in_title:
        evidence.append("overview/framing term appears in title")
    if overview_in_summary:
        evidence.append("overview/framing term appears in abstract")

    if world_in_title and overview_in_title:
        return "high", evidence
    if world_in_title and overview_in_summary:
        return "medium", evidence
    return "low", evidence
