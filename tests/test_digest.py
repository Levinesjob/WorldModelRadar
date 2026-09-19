"""Digest generation with fixtures (offline)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from radar.adapters import AdapterContext, run_adapters_parallel
from radar.digest import DIGEST_BLOCKS, build_digest, render_digest_markdown, write_digest
from radar.paths import CLUSTERS_FILE, FIXTURES_DIR, PAPERS_FILE
from radar.runtime import default_adapters, load_clusters, load_papers, run_pipeline
from radar.schemas import ChannelResult, ChannelStatus, RunStatus
from radar.triage import build_triage_queue


class DigestTests(unittest.TestCase):
    def test_digest_has_five_blocks(self):
        results = [
            ChannelResult("arxiv", "discovery", ChannelStatus.SUCCESS, 1),
            ChannelResult("openreview", "discovery", ChannelStatus.EMPTY),
            ChannelResult("github", "discovery", ChannelStatus.SUCCESS, 1),
            ChannelResult("hackernews", "signal", ChannelStatus.UNAVAILABLE, error_code="timeout"),
        ]
        digest = build_digest(
            run_status=RunStatus.PARTIAL,
            channel_results=results,
            briefs=[
                {
                    "id": "brief-1",
                    "title": "Example",
                    "claim": "主张",
                    "map_position": "definition · core",
                    "do": "研 — 跟",
                    "evidence_links": ["https://arxiv.org/abs/x"],
                    "cluster_id": "definition",
                }
            ],
            candidates=[
                {
                    "title": "Watch me",
                    "url": "https://example.com",
                    "channels": ["github"],
                    "confidence": "medium",
                    "priority_boost": 1.0,
                    "seeded_from_verified": False,
                }
            ],
            clusters=load_clusters(CLUSTERS_FILE),
            week="2026-09-19",
        )
        for key in DIGEST_BLOCKS:
            self.assertIn(key, digest["blocks"])
        self.assertEqual(digest["run_status"], "partial")
        health = digest["blocks"]["pipeline_health"]
        hn = next(r for r in health if r["channel"] == "hackernews")
        self.assertEqual(hn["status"], "unavailable")
        self.assertIn("不可用", hn["reader_copy"])
        self.assertLessEqual(len(digest["blocks"]["watchlist"]), 5)

        md = render_digest_markdown(digest)
        self.assertIn("一句话判断", md)
        self.assertIn("管道健康", md)
        self.assertIn("不可用 ≠ 零候选", md)

    def test_channel_down_judgment_not_zero_news(self):
        results = [
            ChannelResult("arxiv", "discovery", ChannelStatus.UNAVAILABLE),
            ChannelResult("openreview", "discovery", ChannelStatus.UNAVAILABLE),
            ChannelResult("github", "discovery", ChannelStatus.ERROR),
        ]
        digest = build_digest(
            run_status=RunStatus.CHANNEL_DOWN,
            channel_results=results,
            briefs=[],
            candidates=[],
            week="2026-09-19",
        )
        judgment = digest["blocks"]["one_line_judgment"]
        self.assertIn("管道", judgment)
        self.assertNotIn("领域无新闻", judgment.replace("不是「领域无新闻」", ""))

    def test_fixture_pipeline_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifacts = run_pipeline(
                use_fixtures=True,
                fixtures_dir=FIXTURES_DIR,
                papers_path=PAPERS_FILE,
                runs_dir=tmp_path / "runs",
                triage_dir=tmp_path / "triage",
                briefs_dir=tmp_path / "briefs",
                digests_dir=tmp_path / "digests",
            )
            self.assertIn(artifacts.status, (RunStatus.SUCCESS, RunStatus.PARTIAL))
            self.assertTrue(artifacts.run_manifest_path.exists())
            self.assertTrue(artifacts.triage_path.exists())
            self.assertTrue(artifacts.digest_md and artifacts.digest_md.exists())
            self.assertGreaterEqual(artifacts.brief_count, 19)
            manifest = json.loads(artifacts.run_manifest_path.read_text(encoding="utf-8"))
            self.assertIn("status", manifest)
            self.assertEqual(len(manifest["channels"]), 5)
            # Unavailable must never be narrated via missing status field
            for ch in manifest["channels"]:
                self.assertIn(ch["status"], {"success", "empty", "unavailable", "error"})


class TriageHeatPolicyTests(unittest.TestCase):
    def test_heat_boosts_priority_not_auto_verified(self):
        ctx = AdapterContext(use_fixtures=True, fixtures_dir=FIXTURES_DIR, known_arxiv_ids=set())
        results = run_adapters_parallel(default_adapters(include_signals=True), ctx)
        candidates = build_triage_queue(results)
        self.assertTrue(candidates)
        for c in candidates:
            self.assertTrue(c.requires_manual_inclusion_review or c.seeded_from_verified)
            self.assertFalse(c.seeded_from_verified)


if __name__ == "__main__":
    unittest.main()
