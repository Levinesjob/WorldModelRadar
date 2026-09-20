"""Hacker News (Algolia) optional signal adapter."""

from __future__ import annotations

import urllib.parse

from radar.adapters import Adapter, AdapterContext
from radar.http_util import fetch_json
from radar.schemas import Signal, utc_now_iso

HN_ALGOLIA = "https://hn.algolia.com/api/v1/search"


def parse_hn_payload(payload: dict) -> list[Signal]:
    hits = payload.get("hits") or []
    signals: list[Signal] = []
    now = utc_now_iso()
    for hit in hits:
        title = hit.get("title") or hit.get("story_title") or ""
        url = hit.get("url") or ""
        object_id = hit.get("objectID") or ""
        if not title:
            continue
        if not url and object_id:
            url = f"https://news.ycombinator.com/item?id={object_id}"
        points = hit.get("points") or 0
        comments = hit.get("num_comments") or 0
        evidence = ["hacker news story match"]
        if points:
            evidence.append(f"points={points}")
        if comments:
            evidence.append(f"comments={comments}")
        confidence = "medium" if (points or 0) >= 20 else "low"
        created = hit.get("created_at") or now
        signals.append(
            Signal(
                id=f"hn:{object_id or title[:40]}",
                channel="hackernews",
                title=title,
                url=url,
                discovered_at=created,
                summary=(hit.get("story_text") or "")[:1000],
                evidence=evidence,
                confidence=confidence,
                metrics={"points": points, "num_comments": comments},
                raw={"objectID": object_id, "created_at": hit.get("created_at")},
            )
        )
    return signals


class HackerNewsAdapter(Adapter):
    name = "hackernews"
    role = "signal"
    endpoint = HN_ALGOLIA

    def discover(self, ctx: AdapterContext) -> list[Signal]:
        fixture = self.fixture_file(ctx, "hn_algolia.json")
        if fixture is not None:
            return parse_hn_payload(fetch_json("fixture://", fixture_path=fixture))

        params = {
            "query": "world model",
            "tags": "story",
            "hitsPerPage": str(min(ctx.max_results, 30)),
        }
        url = f"{HN_ALGOLIA}?{urllib.parse.urlencode(params)}"
        payload = fetch_json(url, timeout=ctx.timeout)
        return parse_hn_payload(payload)
