"""arXiv Export API discovery adapter."""

from __future__ import annotations

import re
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import date

from radar.adapters import Adapter, AdapterContext
from radar.confidence import OVERVIEW_RE, WORLD_RE, assess_discovery_confidence
from radar.http_util import fetch_bytes
from radar.schemas import Signal, utc_now_iso

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}
START_DATE = date(2026, 1, 1)

QUERIES = [
    "all:world AND all:model AND (all:survey OR all:review OR all:roadmap OR all:taxonomy OR all:definition OR all:framework OR all:position)",
    "all:world AND all:models AND (all:survey OR all:review OR all:roadmap OR all:taxonomy OR all:definition OR all:framework OR all:position)",
]


def arxiv_id_from_url(url: str) -> str:
    raw_id = url.rstrip("/").rsplit("/", 1)[-1]
    return re.sub(r"v\d+$", "", raw_id)


def parse_atom(xml_text: bytes, known_ids: set[str] | None = None) -> list[Signal]:
    known = known_ids or set()
    root = ET.fromstring(xml_text)
    signals: list[Signal] = []
    seen: set[str] = set()
    now = utc_now_iso()

    for entry in root.findall("atom:entry", ATOM):
        entry_url = entry.findtext("atom:id", default="", namespaces=ATOM)
        published = entry.findtext("atom:published", default="", namespaces=ATOM)[:10]
        if not published:
            continue
        try:
            if date.fromisoformat(published) < START_DATE:
                continue
        except ValueError:
            continue

        title = " ".join(entry.findtext("atom:title", default="", namespaces=ATOM).split())
        summary = " ".join(entry.findtext("atom:summary", default="", namespaces=ATOM).split())
        text = f"{title}\n{summary}"
        if not WORLD_RE.search(text) or not OVERVIEW_RE.search(text):
            continue

        arxiv_id = arxiv_id_from_url(entry_url)
        if arxiv_id in known or arxiv_id in seen:
            continue
        seen.add(arxiv_id)

        confidence, evidence = assess_discovery_confidence(title, summary)
        abs_url = f"https://arxiv.org/abs/{arxiv_id}"
        signals.append(
            Signal(
                id=f"arxiv:{arxiv_id}",
                channel="arxiv",
                title=title,
                url=abs_url,
                discovered_at=now,
                summary=summary,
                evidence=evidence,
                confidence=confidence,
                anchors={"arxiv_id": arxiv_id, "published": published},
                raw={"entry_url": entry_url},
            )
        )
    return signals


class ArxivAdapter(Adapter):
    name = "arxiv"
    role = "discovery"
    endpoint = ARXIV_API

    def discover(self, ctx: AdapterContext) -> list[Signal]:
        fixture = self.fixture_file(ctx, "arxiv_atom.xml")
        if fixture is not None:
            return parse_atom(fixture.read_bytes(), ctx.known_arxiv_ids)

        # Live: run first query only to stay quota-friendly; Layer A high-precision.
        query = QUERIES[0]
        params = {
            "search_query": query,
            "start": "0",
            "max_results": str(ctx.max_results),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
        xml_text = fetch_bytes(url, timeout=ctx.timeout)
        return parse_atom(xml_text, ctx.known_arxiv_ids)
