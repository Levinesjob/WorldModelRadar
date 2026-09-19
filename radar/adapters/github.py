"""GitHub discovery adapter (topics / code search for artifacts)."""

from __future__ import annotations

import os
import urllib.parse

from radar.adapters import Adapter, AdapterContext
from radar.http_util import fetch_json
from radar.schemas import Signal, utc_now_iso

GITHUB_SEARCH = "https://api.github.com/search/repositories"


def parse_github_payload(payload: dict) -> list[Signal]:
    items = payload.get("items") or []
    signals: list[Signal] = []
    now = utc_now_iso()
    for item in items:
        full_name = item.get("full_name") or ""
        html_url = item.get("html_url") or ""
        if not full_name or not html_url:
            continue
        description = item.get("description") or ""
        topics = item.get("topics") or []
        stars = item.get("stargazers_count") or 0
        evidence = ["github repository search hit"]
        if any("world" in t and "model" in t for t in topics):
            evidence.append("world-models topic present")
        if "world model" in f"{full_name} {description}".lower():
            evidence.append("world-model phrase in name/description")

        confidence = "medium" if stars >= 50 or len(evidence) > 1 else "low"
        signals.append(
            Signal(
                id=f"github:{full_name}",
                channel="github",
                title=full_name,
                url=html_url,
                discovered_at=now,
                summary=description,
                evidence=evidence,
                confidence=confidence,
                anchors={"repo": full_name},
                metrics={
                    "stars": stars,
                    "forks": item.get("forks_count") or 0,
                    "updated_at": item.get("updated_at") or "",
                    "topics": topics,
                },
                raw={"id": item.get("id")},
            )
        )
    return signals


class GitHubAdapter(Adapter):
    name = "github"
    role = "discovery"
    endpoint = GITHUB_SEARCH

    def discover(self, ctx: AdapterContext) -> list[Signal]:
        fixture = self.fixture_file(ctx, "github_search.json")
        if fixture is not None:
            return parse_github_payload(fetch_json("fixture://", fixture_path=fixture))

        query = 'world model OR world-models in:name,description,topics'
        params = {
            "q": query,
            "sort": "updated",
            "order": "desc",
            "per_page": str(min(ctx.max_results, 30)),
        }
        url = f"{GITHUB_SEARCH}?{urllib.parse.urlencode(params)}"
        headers = {"Accept": "application/vnd.github+json"}
        token = ctx.github_token or os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        payload = fetch_json(url, timeout=ctx.timeout, headers=headers)
        return parse_github_payload(payload)
