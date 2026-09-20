"""Hugging Face Papers optional signal adapter."""

from __future__ import annotations

from radar.adapters import Adapter, AdapterContext
from radar.http_util import fetch_json
from radar.schemas import Signal, utc_now_iso

HF_DAILY = "https://huggingface.co/api/daily_papers"


def parse_hf_payload(payload) -> list[Signal]:
    # API returns a list of { paper, ... } or similar shapes.
    items = payload if isinstance(payload, list) else payload.get("papers") or payload.get("items") or []
    signals: list[Signal] = []
    now = utc_now_iso()

    for item in items:
        paper = item.get("paper") if isinstance(item, dict) else None
        if paper is None and isinstance(item, dict):
            paper = item
        if not isinstance(paper, dict):
            continue

        title = paper.get("title") or ""
        arxiv_id = (
            paper.get("id")
            or paper.get("arxiv_id")
            or (paper.get("arxiv") or {}).get("id")
            or ""
        )
        if isinstance(arxiv_id, dict):
            arxiv_id = arxiv_id.get("id") or ""
        arxiv_id = str(arxiv_id).removeprefix("arxiv:")

        text = f"{title} {paper.get('summary') or paper.get('abstract') or ''}".lower()
        if "world model" not in text and "world models" not in text and "world modeling" not in text:
            # Keep trending items that explicitly mention world models only.
            continue
        if not title:
            continue

        upvotes = item.get("reactions") or item.get("upvotes") or paper.get("upvotes") or 0
        if isinstance(upvotes, dict):
            upvotes = upvotes.get("count") or 0

        url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else paper.get("url") or ""
        evidence = ["huggingface daily papers hit"]
        if upvotes:
            evidence.append(f"upvotes={upvotes}")
        confidence = "medium" if upvotes else "low"
        anchors = {}
        if arxiv_id:
            anchors["arxiv_id"] = arxiv_id

        published = (
            item.get("publishedAt")
            or item.get("published_at")
            or paper.get("publishedAt")
            or now
        )
        signals.append(
            Signal(
                id=f"hf:{arxiv_id or title[:40]}",
                channel="huggingface",
                title=title,
                url=url or f"https://huggingface.co/papers/{arxiv_id}",
                discovered_at=str(published),
                summary=(paper.get("summary") or paper.get("abstract") or "")[:2000],
                evidence=evidence,
                confidence=confidence,
                anchors=anchors,
                metrics={"upvotes": upvotes},
                raw={"paper_id": paper.get("id"), "publishedAt": published},
            )
        )
    return signals


class HuggingFaceAdapter(Adapter):
    name = "huggingface"
    role = "signal"
    endpoint = HF_DAILY

    def discover(self, ctx: AdapterContext) -> list[Signal]:
        fixture = self.fixture_file(ctx, "hf_daily_papers.json")
        if fixture is not None:
            return parse_hf_payload(fetch_json("fixture://", fixture_path=fixture))

        payload = fetch_json(HF_DAILY, timeout=ctx.timeout)
        return parse_hf_payload(payload)
