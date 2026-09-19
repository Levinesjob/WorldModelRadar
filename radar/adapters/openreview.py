"""OpenReview discovery adapter (public API v2 notes search)."""

from __future__ import annotations

from radar.adapters import Adapter, AdapterContext
from radar.confidence import assess_discovery_confidence
from radar.http_util import fetch_json
from radar.schemas import Signal, utc_now_iso

OPENREVIEW_API = "https://api2.openreview.net/notes/search"


def parse_openreview_payload(payload: dict, known_ids: set[str] | None = None) -> list[Signal]:
    known = known_ids or set()
    notes = payload.get("notes") or payload.get("results") or []
    signals: list[Signal] = []
    now = utc_now_iso()
    seen: set[str] = set()

    for note in notes:
        content = note.get("content") or {}
        title = _field_value(content.get("title")) or note.get("title") or ""
        abstract = _field_value(content.get("abstract")) or ""
        if not title:
            continue
        text = f"{title}\n{abstract}".lower()
        if "world model" not in text and "world models" not in text and "world modeling" not in text:
            continue

        forum = note.get("forum") or note.get("id") or ""
        if not forum or forum in seen:
            continue
        seen.add(forum)

        # Prefer arXiv id from content if present.
        arxiv_id = _field_value(content.get("arxiv")) or ""
        if arxiv_id.startswith("http"):
            arxiv_id = arxiv_id.rstrip("/").rsplit("/", 1)[-1]
        if arxiv_id and arxiv_id in known:
            continue

        confidence, evidence = assess_discovery_confidence(title, abstract)
        evidence = list(evidence) + ["openreview forum hit"]
        url = f"https://openreview.net/forum?id={forum}"
        anchors = {"openreview_forum": forum}
        if arxiv_id:
            anchors["arxiv_id"] = arxiv_id

        signals.append(
            Signal(
                id=f"openreview:{forum}",
                channel="openreview",
                title=title,
                url=url,
                discovered_at=now,
                summary=abstract[:2000],
                evidence=evidence,
                confidence=confidence,
                anchors=anchors,
                metrics={"num_replies": note.get("number") or 0},
                raw={"id": note.get("id")},
            )
        )
    return signals


def _field_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return str(value.get("value") or "")
    return str(value)


class OpenReviewAdapter(Adapter):
    name = "openreview"
    role = "discovery"
    endpoint = OPENREVIEW_API

    def discover(self, ctx: AdapterContext) -> list[Signal]:
        fixture = self.fixture_file(ctx, "openreview_search.json")
        if fixture is not None:
            return parse_openreview_payload(fetch_json("fixture://", fixture_path=fixture), ctx.known_arxiv_ids)

        # Public search; may be rate-limited — failures become unavailable upstream.
        url = (
            f"{OPENREVIEW_API}?term=world%20model&limit={ctx.max_results}"
            "&content=all&source=forum"
        )
        payload = fetch_json(url, timeout=ctx.timeout)
        return parse_openreview_payload(payload, ctx.known_arxiv_ids)
