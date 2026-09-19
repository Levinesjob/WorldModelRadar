"""Brief generation and schema validation helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from radar.schemas import Brief, validate_brief

# Map paper area keywords → cluster ids (see data/clusters.json).
AREA_CLUSTER_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"robot|embodied|action model|physical intelligence|vla", re.I), "robot"),
    (re.compile(r"driv|counterfactual|autonom", re.I), "robot"),
    (re.compile(r"video|generative foundation|interactive video", re.I), "video_sim"),
    (re.compile(r"simulat|admissib|physical grounding|actionable", re.I), "runtime"),
    (re.compile(r"evaluat|benchmark|decision-making-centric", re.I), "eval"),
    (re.compile(r"definition|roadmap|taxonomy|framing|openworldlib|graph world", re.I), "definition"),
    (re.compile(r"code|openworldlib|unified codebase", re.I), "code"),
    (re.compile(r"medical|economic|edge|digital twin", re.I), "runtime"),
]


def infer_cluster(area: str, title: str = "") -> str:
    text = f"{area} {title}"
    for pattern, cluster_id in AREA_CLUSTER_RULES:
        if pattern.search(text):
            return cluster_id
    return "definition"


def do_from_relevance(relevance: str) -> str:
    if relevance == "core":
        return "研 — 领域级 framing，值得跟定义与评价争论"
    if relevance == "domain":
        return "观望 — 领域切片，跟场景成熟度与可迁移协议"
    return "忽略 — adjacent；仅作边界对照，不进主清单决策"


def brief_from_paper(paper: dict[str, Any]) -> Brief:
    """Derive a scannable Chinese brief from a verified paper record."""
    paper_id = paper.get("id") or ""
    title = paper.get("title") or ""
    area = paper.get("area") or ""
    why = paper.get("why_included") or ""
    relevance = paper.get("relevance") or "adjacent"
    cluster = infer_cluster(area, title)

    # Keep claim ≤150 chars; prefer why_included compressed.
    claim_src = why if why else title
    claim = claim_src if len(claim_src) <= 150 else claim_src[:147] + "…"

    evidence = []
    if paper.get("url"):
        evidence.append(paper["url"])
    if paper.get("repository"):
        evidence.append(paper["repository"])
    if not evidence and paper.get("arxiv_id"):
        evidence.append(f"https://arxiv.org/abs/{paper['arxiv_id']}")

    return Brief(
        id=f"brief-{paper_id}",
        paper_id=paper_id,
        title=title,
        claim=claim,
        map_position=f"{cluster} · {relevance} · {area}",
        do=do_from_relevance(relevance),
        fake_demand="把讨论热度或星标当成收录理由（热度只提权，不单独进 Verified）",
        evidence_links=evidence,
        cluster_id=cluster,
    )


def write_brief(path: Path, brief: Brief) -> list[str]:
    """Validate and write brief JSON. Returns validation errors (empty if ok)."""
    payload = brief.to_dict()
    errors = validate_brief(payload)
    if errors:
        return errors
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return []


def load_briefs(briefs_dir: Path) -> list[dict[str, Any]]:
    if not briefs_dir.exists():
        return []
    briefs = []
    for path in sorted(briefs_dir.glob("*.json")):
        briefs.append(json.loads(path.read_text(encoding="utf-8")))
    return briefs


def seed_briefs_from_papers(papers: list[dict[str, Any]], briefs_dir: Path) -> tuple[int, list[str]]:
    """Generate brief files for all papers; return (written, error messages)."""
    written = 0
    errors: list[str] = []
    briefs_dir.mkdir(parents=True, exist_ok=True)
    for paper in papers:
        brief = brief_from_paper(paper)
        path = briefs_dir / f"{brief.paper_id}.json"
        errs = write_brief(path, brief)
        if errs:
            errors.append(f"{brief.paper_id}: {', '.join(errs)}")
        else:
            written += 1
    return written, errors
