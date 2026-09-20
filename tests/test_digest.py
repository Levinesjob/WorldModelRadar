"""Secretary briefing (Digest) generation with fixtures (offline)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from radar.adapters import AdapterContext, run_adapters_parallel
from radar.digest import DIGEST_BLOCKS, build_digest, render_digest_markdown
from radar.paths import CLUSTERS_FILE, FIXTURES_DIR, PAPERS_FILE
from radar.runtime import default_adapters, load_clusters, run_pipeline
from radar.schemas import ChannelResult, ChannelStatus, RunStatus, Signal, channel_health_label
from radar.triage import build_triage_queue


def _signal(channel: str, sid: str, title: str, *, when: str = "2026-09-18T00:00:00+00:00") -> Signal:
    return Signal(
        id=sid,
        channel=channel,
        title=title,
        url=f"https://example.com/{sid}",
        discovered_at=when,
        confidence="medium",
        evidence=["test"],
    )


class DigestTests(unittest.TestCase):
    def test_digest_has_secretary_blocks(self):
        results = [
            ChannelResult(
                "arxiv",
                "discovery",
                ChannelStatus.SUCCESS,
                1,
                signals=[_signal("arxiv", "arxiv:1", "Arxiv Hit")],
            ),
            ChannelResult("openreview", "discovery", ChannelStatus.EMPTY),
            ChannelResult("github", "discovery", ChannelStatus.SUCCESS, 1),
            ChannelResult(
                "hackernews",
                "signal",
                ChannelStatus.UNAVAILABLE,
                error_code="timeout",
            ),
            ChannelResult(
                "huggingface",
                "signal",
                ChannelStatus.SUCCESS,
                1,
                signals=[_signal("huggingface", "hf:1", "HF World Model Paper")],
            ),
        ]
        digest = build_digest(
            run_status=RunStatus.PARTIAL,
            channel_results=results,
            briefs=[
                {
                    "id": "brief-1",
                    "title": "Example Title",
                    "claim": "中文主张：世界模型需要可行动模拟。",
                    "map_position": "definition · core",
                    "do": "研 — 跟定义争论",
                    "fake_demand": "勿把热度当收录理由",
                    "evidence_links": ["https://arxiv.org/abs/x"],
                    "cluster_id": "definition",
                    "horizon": "mainline",
                    "mainline_note": "改写 runtime 契约，进入主线。",
                },
                {
                    "id": "brief-2",
                    "title": "Domain Slice",
                    "claim": "某领域局部协议补丁。",
                    "map_position": "robot · domain",
                    "do": "观望 — 跟场景成熟度",
                    "fake_demand": "勿升格为主线",
                    "evidence_links": ["https://arxiv.org/abs/y"],
                    "cluster_id": "robot",
                    "horizon": "near_term",
                    "mainline_note": "局部优化，不改长期主线。",
                },
            ],
            candidates=[
                {
                    "id": "cand-1",
                    "title": "HF World Model Paper",
                    "url": "https://example.com/hf:1",
                    "channels": ["huggingface"],
                    "confidence": "medium",
                    "priority_boost": 1.0,
                    "seeded_from_verified": False,
                    "signal_ids": ["hf:1"],
                }
            ],
            clusters=load_clusters(CLUSTERS_FILE),
            week="2026-09-19",
        )
        for key in DIGEST_BLOCKS:
            self.assertIn(key, digest["blocks"])

        self.assertEqual(digest["run_status"], "partial")
        self.assertEqual(digest["product"], "secretary_briefing")
        self.assertGreaterEqual(len(digest["blocks"]["judgment"]), 1)
        self.assertLessEqual(len(digest["blocks"]["judgment"]), 3)

        mainline = digest["blocks"]["mainline"]
        self.assertTrue(mainline)
        self.assertEqual(mainline[0]["horizon"], "mainline")
        self.assertIn("主线", mainline[0]["mainline_note"])

        near = digest["blocks"]["near_term"]
        self.assertTrue(near)
        self.assertEqual(near[0]["horizon"], "near_term")

        health = digest["blocks"]["pipeline_health"]
        hn = next(r for r in health if r["channel"] == "hackernews")
        self.assertEqual(hn["status"], "unavailable")
        self.assertEqual(hn["health"], "unavailable")
        self.assertIn("不可用", hn["reader_copy"])

        heat = digest["blocks"]["heat_radar"]
        self.assertTrue(heat["hits"])
        self.assertEqual(heat["hits"][0]["source"], "heat_or_discovery")
        self.assertIn("huggingface", heat["hits"][0]["channels"])
        self.assertTrue(heat["coverage"])

        md = render_digest_markdown(digest)
        self.assertIn("秘书周报", md)
        self.assertIn("今日/本周判断", md)
        self.assertIn("主线动态", md)
        self.assertIn("短期局部", md)
        self.assertIn("热源雷达", md)
        self.assertIn("缺口与下周盯梢", md)
        self.assertIn("管道健康", md)
        self.assertIn("主线/长期", md)
        self.assertIn("短期/局部", md)
        self.assertIn("主线影响", md)
        self.assertIn("不可用 ≠ 零候选", md)
        self.assertIn("`unavailable`", md)
        self.assertIn("HF World Model Paper", md)
        self.assertIn("为何看", md)

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
        judgment = " ".join(digest["blocks"]["judgment"])
        self.assertIn("管道", judgment)
        self.assertIn("不是「领域无新闻」", judgment)

    def test_heat_not_dumped_into_mainline(self):
        results = [
            ChannelResult(
                "hackernews",
                "signal",
                ChannelStatus.SUCCESS,
                1,
                signals=[_signal("hackernews", "hn:1", "Hot HN Thread")],
            ),
        ]
        digest = build_digest(
            run_status=RunStatus.SUCCESS,
            channel_results=[
                ChannelResult("arxiv", "discovery", ChannelStatus.EMPTY),
                ChannelResult("openreview", "discovery", ChannelStatus.EMPTY),
                ChannelResult("github", "discovery", ChannelStatus.EMPTY),
                *results,
            ],
            briefs=[
                {
                    "id": "b1",
                    "claim": "主线主张",
                    "do": "研 — x",
                    "map_position": "definition · core",
                    "evidence_links": ["https://example.com"],
                    "cluster_id": "definition",
                    "horizon": "mainline",
                    "mainline_note": "改定义。",
                    "title": "Main",
                }
            ],
            candidates=[
                {
                    "id": "c1",
                    "title": "Hot HN Thread",
                    "url": "https://example.com/hn",
                    "channels": ["hackernews"],
                    "confidence": "medium",
                    "priority_boost": 5.0,
                    "seeded_from_verified": False,
                    "signal_ids": ["hn:1"],
                }
            ],
            week="2026-09-20",
        )
        mainline_titles = {c.get("title") for c in digest["blocks"]["mainline"]}
        self.assertNotIn("Hot HN Thread", mainline_titles)
        heat_titles = {h.get("title") for h in digest["blocks"]["heat_radar"]["hits"]}
        self.assertIn("Hot HN Thread", heat_titles)

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
            by_ch = {c["channel"]: c for c in manifest["channels"]}
            for ch in ("hackernews", "huggingface"):
                self.assertIn(ch, by_ch)
                self.assertIn(by_ch[ch]["health"], {"ok", "unavailable", "partial"})
                self.assertIn("samples", by_ch[ch])
            self.assertGreaterEqual(by_ch["hackernews"]["item_count"], 2)
            self.assertTrue(by_ch["hackernews"]["samples"])
            hn_titles = {s["title"] for s in by_ch["hackernews"]["samples"]}
            self.assertTrue(any("world model" in t.lower() or "WorldModel" in t for t in hn_titles))
            self.assertGreaterEqual(by_ch["huggingface"]["item_count"], 2)
            hf_ids = {s["id"] for s in by_ch["huggingface"]["samples"]}
            self.assertTrue(any(i.startswith("hf:") for i in hf_ids))

            digest_md = artifacts.digest_md.read_text(encoding="utf-8")
            self.assertIn("秘书周报", digest_md)
            self.assertIn("主线动态", digest_md)
            self.assertIn("短期局部", digest_md)
            self.assertIn("热源雷达", digest_md)
            self.assertIn("Hacker News", digest_md)
            self.assertIn("Hugging Face", digest_md)
            self.assertIn("Open-source world model simulator", digest_md)
            self.assertIn("WorldModelBench", digest_md)
            self.assertIn("Latent World Models for Robot Rollouts", digest_md)
            self.assertIn("主线影响", digest_md)

            digest_json = json.loads(artifacts.digest_json.read_text(encoding="utf-8"))
            self.assertIn("heat_radar", digest_json["blocks"])
            self.assertTrue(digest_json["blocks"]["heat_radar"]["hits"])
            self.assertTrue(digest_json["blocks"]["mainline"])
            for card in digest_json["blocks"]["mainline"]:
                self.assertEqual(card["horizon"], "mainline")
                self.assertTrue(card.get("mainline_note"))
                self.assertTrue(card.get("claim"))
            for card in digest_json["blocks"]["near_term"]:
                self.assertEqual(card["horizon"], "near_term")
            self.assertLessEqual(len(digest_json["blocks"]["judgment"]), 3)
            self.assertLessEqual(len(digest_json["blocks"]["mainline"]), 5)
            self.assertLessEqual(len(digest_json["blocks"]["near_term"]), 5)

            for ch in manifest["channels"]:
                self.assertIn(ch["status"], {"success", "empty", "unavailable", "error"})


class ChannelHealthLabelTests(unittest.TestCase):
    def test_health_mapping(self):
        self.assertEqual(channel_health_label(ChannelStatus.SUCCESS), "ok")
        self.assertEqual(channel_health_label(ChannelStatus.EMPTY), "ok")
        self.assertEqual(channel_health_label(ChannelStatus.UNAVAILABLE), "unavailable")
        self.assertEqual(channel_health_label(ChannelStatus.ERROR), "partial")


class TriageHeatPolicyTests(unittest.TestCase):
    def test_heat_boosts_priority_not_auto_verified(self):
        ctx = AdapterContext(use_fixtures=True, fixtures_dir=FIXTURES_DIR, known_arxiv_ids=set())
        results = run_adapters_parallel(default_adapters(include_signals=True), ctx)
        candidates = build_triage_queue(results)
        self.assertTrue(candidates)
        for c in candidates:
            self.assertTrue(c.requires_manual_inclusion_review or c.seeded_from_verified)
            self.assertFalse(c.seeded_from_verified)
        heat_channels = {ch for c in candidates for ch in c.channels}
        self.assertIn("hackernews", heat_channels)
        self.assertIn("huggingface", heat_channels)


class FixtureSignalDistinctnessTests(unittest.TestCase):
    def test_hn_hf_fixtures_not_ledger_copies(self):
        papers = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
        ledger_titles = {p["title"] for p in papers}
        ledger_arxiv = {p.get("arxiv_id") for p in papers if p.get("arxiv_id")}

        hn = json.loads((FIXTURES_DIR / "hn_algolia.json").read_text(encoding="utf-8"))
        hn_titles = {h["title"] for h in hn["hits"]}
        self.assertTrue(hn_titles.isdisjoint(ledger_titles))

        hf = json.loads((FIXTURES_DIR / "hf_daily_papers.json").read_text(encoding="utf-8"))
        hf_ids = {item["paper"]["id"] for item in hf}
        self.assertIn("2609.77777", hf_ids)
        self.assertNotIn("2609.77777", ledger_arxiv)
        self.assertIn("2609.99999", hf_ids)
        self.assertNotIn("2609.99999", ledger_arxiv)


if __name__ == "__main__":
    unittest.main()
