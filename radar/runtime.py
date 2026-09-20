"""Radar Runtime orchestrator: discover → triage → brief → digest → run status."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from radar.adapters import AdapterContext, run_adapters_parallel
from radar.adapters.arxiv import ArxivAdapter
from radar.adapters.github import GitHubAdapter
from radar.adapters.hackernews import HackerNewsAdapter
from radar.adapters.huggingface import HuggingFaceAdapter
from radar.adapters.openreview import OpenReviewAdapter
from radar.brief import load_briefs, seed_briefs_from_papers
from radar.digest import build_digest, write_digest
from radar.paths import (
    BRIEFS_DIR,
    CLUSTERS_FILE,
    DIGESTS_DIR,
    FIXTURES_DIR,
    PAPERS_FILE,
    RUNS_DIR,
    TRIAGE_DIR,
)
from radar.schemas import (
    ChannelResult,
    RunStatus,
    aggregate_run_status,
    channel_health_label,
    channel_samples,
    utc_now_iso,
)
from radar.triage import build_triage_queue, candidates_from_papers, write_triage_queue


@dataclass
class RunArtifacts:
    run_id: str
    status: RunStatus
    run_manifest_path: Path
    triage_path: Path
    digest_json: Path | None
    digest_md: Path | None
    channel_results: list[ChannelResult]
    candidate_count: int
    brief_count: int


def load_papers(path: Path = PAPERS_FILE) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_clusters(path: Path = CLUSTERS_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("clusters", data if isinstance(data, list) else [])


def default_adapters(*, include_signals: bool = True) -> list:
    adapters = [ArxivAdapter(), OpenReviewAdapter(), GitHubAdapter()]
    if include_signals:
        adapters.extend([HackerNewsAdapter(), HuggingFaceAdapter()])
    return adapters


def write_run_manifest(
    path: Path,
    *,
    run_id: str,
    status: RunStatus,
    channel_results: list[ChannelResult],
    candidate_count: int,
    brief_count: int,
    mode: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": run_id,
        "started_at": run_id,  # ISO date or datetime used as id
        "finished_at": utc_now_iso(),
        "status": status.value,
        "mode": mode,
        "candidate_count": candidate_count,
        "brief_count": brief_count,
        "channels": [
            {
                "channel": r.channel,
                "role": r.role,
                "status": r.status.value,
                "health": channel_health_label(r.status),
                "item_count": r.item_count,
                "error_code": r.error_code,
                "message": r.message,
                "duration_ms": r.duration_ms,
                "endpoint": r.endpoint,
                "samples": channel_samples(r, limit=3),
                "latest_discovered_at": max(
                    (s.discovered_at for s in r.signals if s.discovered_at),
                    default=None,
                ),
            }
            for r in channel_results
        ],
        "notes": {
            "unavailable_means": "channel outage — not an empty field / not zero candidates",
            "heat_policy": "signal heat boosts triage priority only; never sole verified inclusion",
            "verified_vs_signals": (
                "Verified Briefs come from data/papers.json ledger; "
                "new signals this run come from discovery/heat adapters (HN Algolia, HF Papers, etc.)"
            ),
            "live_heat_endpoints": {
                "hackernews": "https://hn.algolia.com/api/v1/search (query=world model, tags=story)",
                "huggingface": "https://huggingface.co/api/daily_papers",
            },
            "fixtures_heat": (
                "With --fixtures, HN/HF read data/fixtures/hn_algolia.json and "
                "hf_daily_papers.json — distinct synthetic heat items, not ledger copies"
            ),
        },
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_pipeline(
    *,
    use_fixtures: bool = False,
    include_signals: bool = True,
    seed_briefs: bool = True,
    write_digest_files: bool = True,
    max_results: int = 25,
    fixtures_dir: Path | None = None,
    papers_path: Path = PAPERS_FILE,
    runs_dir: Path = RUNS_DIR,
    triage_dir: Path = TRIAGE_DIR,
    briefs_dir: Path = BRIEFS_DIR,
    digests_dir: Path = DIGESTS_DIR,
    judgment: str | None = None,
) -> RunArtifacts:
    papers = load_papers(papers_path)
    known_ids = {p.get("arxiv_id", "") for p in papers if p.get("arxiv_id")}
    clusters = load_clusters()

    if seed_briefs:
        seed_briefs_from_papers(papers, briefs_dir)

    ctx = AdapterContext(
        use_fixtures=use_fixtures,
        fixtures_dir=fixtures_dir or FIXTURES_DIR,
        max_results=max_results,
        github_token=os.environ.get("GITHUB_TOKEN"),
        known_arxiv_ids=known_ids,
    )
    adapters = default_adapters(include_signals=include_signals)
    channel_results = run_adapters_parallel(adapters, ctx)

    seed = candidates_from_papers(papers)
    # For triage of *new* work, seed is available but we primarily surface non-seed
    # from live signals; include seed only as reference when fixtures/demo needs it.
    candidates = build_triage_queue(channel_results, seed_candidates=None)
    # Attach seed separately in triage file meta; keep queue focused on discovery+signal.
    # Still expose seed count for Digest watchlist fallback via verified briefs.

    run_id = utc_now_iso()
    status = aggregate_run_status(channel_results)
    mode = "fixtures" if use_fixtures else "live"

    triage_path = triage_dir / f"{date.today().isoformat()}.json"
    write_triage_queue(
        triage_path,
        candidates,
        meta={
            "run_id": run_id,
            "run_status": status.value,
            "mode": mode,
            "verified_seed_count": len(seed),
            "note": "Heat signals boost priority only; verified inclusion still requires primary-source gate.",
        },
    )

    briefs = load_briefs(briefs_dir)
    digest_json = digest_md = None
    if write_digest_files:
        digest = build_digest(
            run_status=status,
            channel_results=channel_results,
            briefs=briefs,
            candidates=[c.to_dict() for c in candidates],
            clusters=clusters,
            judgment=judgment,
            week=date.today().isoformat(),
        )
        digest_json, digest_md = write_digest(digests_dir, digest)

    manifest_path = runs_dir / f"{date.today().isoformat()}.json"
    # If multiple runs same day, also write timestamped copy.
    stamp_path = runs_dir / f"{run_id.replace(':', '')}.json"
    write_run_manifest(
        manifest_path,
        run_id=run_id,
        status=status,
        channel_results=channel_results,
        candidate_count=len(candidates),
        brief_count=len(briefs),
        mode=mode,
    )
    write_run_manifest(
        stamp_path,
        run_id=run_id,
        status=status,
        channel_results=channel_results,
        candidate_count=len(candidates),
        brief_count=len(briefs),
        mode=mode,
    )

    return RunArtifacts(
        run_id=run_id,
        status=status,
        run_manifest_path=manifest_path,
        triage_path=triage_path,
        digest_json=digest_json,
        digest_md=digest_md,
        channel_results=channel_results,
        candidate_count=len(candidates),
        brief_count=len(briefs),
    )
