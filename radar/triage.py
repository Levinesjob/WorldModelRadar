"""Build triage queue from channel signals + optional verified seed."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from radar.schemas import Candidate, ChannelResult, ChannelStatus, Signal

CONFIDENCE_RANK = {"high": 3, "medium": 2, "low": 1}


def _dedupe_key(signal: Signal) -> str:
    if signal.anchors.get("arxiv_id"):
        return f"arxiv:{signal.anchors['arxiv_id']}"
    if signal.anchors.get("repo"):
        return f"repo:{signal.anchors['repo']}"
    if signal.anchors.get("openreview_forum"):
        return f"or:{signal.anchors['openreview_forum']}"
    return f"url:{signal.url or signal.title}"


def _merge_confidence(a: str, b: str) -> str:
    return a if CONFIDENCE_RANK.get(a, 0) >= CONFIDENCE_RANK.get(b, 0) else b


def signals_from_results(results: list[ChannelResult]) -> list[Signal]:
    """Collect signals only from healthy channels (success). Unavailable ≠ empty."""
    out: list[Signal] = []
    for result in results:
        if result.status == ChannelStatus.SUCCESS:
            out.extend(result.signals)
    return out


def build_triage_queue(
    results: list[ChannelResult],
    *,
    seed_candidates: list[Candidate] | None = None,
) -> list[Candidate]:
    """Merge signals into candidates; heat channels only boost priority."""
    by_key: dict[str, Candidate] = {}

    for signal in signals_from_results(results):
        key = _dedupe_key(signal)
        boost = 0.0
        if signal.channel in ("hackernews", "huggingface"):
            # Heat is priority-only — never sole inclusion (seeded_from_verified stays False).
            boost = 1.0
            if signal.channel == "hackernews":
                boost += min(float(signal.metrics.get("points") or 0) / 100.0, 2.0)
            if signal.channel == "huggingface":
                boost += min(float(signal.metrics.get("upvotes") or 0) / 50.0, 2.0)

        if key not in by_key:
            cand_id = hashlib.sha1(key.encode()).hexdigest()[:12]
            by_key[key] = Candidate(
                id=f"cand-{cand_id}",
                title=signal.title,
                url=signal.url,
                channels=[signal.channel],
                confidence=signal.confidence,
                evidence=list(signal.evidence),
                signal_ids=[signal.id],
                anchors=dict(signal.anchors),
                summary=signal.summary,
                priority_boost=boost,
            )
        else:
            cand = by_key[key]
            if signal.channel not in cand.channels:
                cand.channels.append(signal.channel)
            if signal.id not in cand.signal_ids:
                cand.signal_ids.append(signal.id)
            cand.confidence = _merge_confidence(cand.confidence, signal.confidence)
            for e in signal.evidence:
                if e not in cand.evidence:
                    cand.evidence.append(e)
            cand.anchors.update({k: v for k, v in signal.anchors.items() if v})
            cand.priority_boost += boost
            if not cand.summary and signal.summary:
                cand.summary = signal.summary

    candidates = list(by_key.values())

    if seed_candidates:
        existing_keys = {_seed_key(c) for c in candidates}
        for seed in seed_candidates:
            sk = _seed_key(seed)
            if sk not in existing_keys:
                candidates.append(seed)
                existing_keys.add(sk)

    candidates.sort(
        key=lambda c: (
            CONFIDENCE_RANK.get(c.confidence, 0) + c.priority_boost,
            c.title.lower(),
        ),
        reverse=True,
    )
    return candidates


def _seed_key(cand: Candidate) -> str:
    if cand.anchors.get("arxiv_id"):
        return f"arxiv:{cand.anchors['arxiv_id']}"
    return f"url:{cand.url or cand.title}"


def candidates_from_papers(papers: list[dict[str, Any]]) -> list[Candidate]:
    """Migrate verified papers.json into triage seed (already verified, still reviewable)."""
    out: list[Candidate] = []
    for paper in papers:
        arxiv_id = paper.get("arxiv_id") or ""
        out.append(
            Candidate(
                id=f"seed-{paper.get('id', arxiv_id)}",
                title=paper.get("title") or "",
                url=paper.get("url") or "",
                channels=["verified_ledger"],
                confidence="high",
                evidence=[
                    "seeded from verified papers.json",
                    paper.get("why_included") or "",
                ],
                signal_ids=[],
                anchors={"arxiv_id": arxiv_id, "paper_id": paper.get("id") or ""},
                summary=paper.get("why_included") or "",
                priority_boost=0.0,
                requires_manual_inclusion_review=False,
                seeded_from_verified=True,
            )
        )
    return out


def write_triage_queue(path: Path, candidates: list[Candidate], meta: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        **meta,
        "candidate_count": len(candidates),
        "candidates": [c.to_dict() for c in candidates],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
