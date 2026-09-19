"""Offline unit tests: adapter isolation."""

from __future__ import annotations

import unittest
from pathlib import Path

from radar.adapters import AdapterContext, failing_adapter, ok_adapter, run_adapter, run_adapters_parallel
from radar.adapters.arxiv import ArxivAdapter, parse_atom
from radar.adapters.github import GitHubAdapter, parse_github_payload
from radar.adapters.hackernews import HackerNewsAdapter
from radar.adapters.huggingface import HuggingFaceAdapter
from radar.adapters.openreview import OpenReviewAdapter, parse_openreview_payload
from radar.http_util import HttpError
from radar.paths import FIXTURES_DIR, ROOT
from radar.schemas import ChannelStatus, Signal


class AdapterIsolationTests(unittest.TestCase):
    def test_one_failing_channel_does_not_stop_others(self):
        adapters = [
            failing_adapter("arxiv", "discovery", HttpError("timeout", "arxiv down")),
            ok_adapter(
                "openreview",
                "discovery",
                [
                    Signal(
                        id="or:1",
                        channel="openreview",
                        title="World Models Position",
                        url="https://openreview.net/forum?id=1",
                        discovered_at="2026-09-19T00:00:00+00:00",
                        confidence="high",
                        evidence=["test"],
                    )
                ],
            ),
            ok_adapter("github", "discovery", []),
        ]
        results = run_adapters_parallel(adapters, AdapterContext())
        by_name = {r.channel: r for r in results}
        self.assertEqual(by_name["arxiv"].status, ChannelStatus.UNAVAILABLE)
        self.assertEqual(by_name["openreview"].status, ChannelStatus.SUCCESS)
        self.assertEqual(by_name["openreview"].item_count, 1)
        self.assertEqual(by_name["github"].status, ChannelStatus.EMPTY)

    def test_http_error_maps_to_unavailable_not_empty(self):
        adapter = failing_adapter("hackernews", "signal", HttpError("http_429", "rate limited", 429))
        result = run_adapter(adapter, AdapterContext())
        self.assertEqual(result.status, ChannelStatus.UNAVAILABLE)
        self.assertEqual(result.error_code, "http_429")
        self.assertEqual(result.item_count, 0)
        self.assertNotEqual(result.message.lower().find("zero"), 0)  # must not claim zero candidates narrative

    def test_fixture_adapters_parse(self):
        ctx = AdapterContext(use_fixtures=True, fixtures_dir=FIXTURES_DIR, known_arxiv_ids={"2608.11601"})
        arxiv = run_adapter(ArxivAdapter(), ctx)
        self.assertEqual(arxiv.status, ChannelStatus.SUCCESS)
        self.assertGreaterEqual(arxiv.item_count, 1)
        self.assertTrue(all(s.anchors.get("arxiv_id") != "2608.11601" for s in arxiv.signals))

        openreview = run_adapter(OpenReviewAdapter(), ctx)
        self.assertEqual(openreview.status, ChannelStatus.SUCCESS)

        github = run_adapter(GitHubAdapter(), ctx)
        self.assertEqual(github.status, ChannelStatus.SUCCESS)

        hn = run_adapter(HackerNewsAdapter(), ctx)
        self.assertEqual(hn.status, ChannelStatus.SUCCESS)

        hf = run_adapter(HuggingFaceAdapter(), ctx)
        self.assertEqual(hf.status, ChannelStatus.SUCCESS)

    def test_parse_atom_filters_non_overview(self):
        xml = (FIXTURES_DIR / "arxiv_atom.xml").read_bytes()
        signals = parse_atom(xml, known_ids=set())
        ids = {s.anchors["arxiv_id"] for s in signals}
        self.assertIn("2609.99999", ids)
        self.assertNotIn("2609.11111", ids)


class FixturePresenceTests(unittest.TestCase):
    def test_fixtures_exist(self):
        for name in [
            "arxiv_atom.xml",
            "openreview_search.json",
            "github_search.json",
            "hn_algolia.json",
            "hf_daily_papers.json",
        ]:
            self.assertTrue((FIXTURES_DIR / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
