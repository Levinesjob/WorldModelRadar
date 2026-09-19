"""Run status aggregation semantics."""

from __future__ import annotations

import unittest

from radar.schemas import ChannelResult, ChannelStatus, RunStatus, aggregate_run_status, status_reader_copy


def _ch(name: str, role: str, status: ChannelStatus, n: int = 0) -> ChannelResult:
    return ChannelResult(channel=name, role=role, status=status, item_count=n)


class StatusSemanticsTests(unittest.TestCase):
    def test_all_discovery_success_is_success(self):
        results = [
            _ch("arxiv", "discovery", ChannelStatus.SUCCESS, 2),
            _ch("openreview", "discovery", ChannelStatus.EMPTY),
            _ch("github", "discovery", ChannelStatus.SUCCESS, 1),
            _ch("hackernews", "signal", ChannelStatus.SUCCESS, 3),
        ]
        self.assertEqual(aggregate_run_status(results), RunStatus.SUCCESS)

    def test_one_discovery_down_is_partial(self):
        results = [
            _ch("arxiv", "discovery", ChannelStatus.UNAVAILABLE),
            _ch("openreview", "discovery", ChannelStatus.SUCCESS, 1),
            _ch("github", "discovery", ChannelStatus.SUCCESS, 1),
        ]
        self.assertEqual(aggregate_run_status(results), RunStatus.PARTIAL)

    def test_all_discovery_down_is_channel_down(self):
        results = [
            _ch("arxiv", "discovery", ChannelStatus.UNAVAILABLE),
            _ch("openreview", "discovery", ChannelStatus.ERROR),
            _ch("github", "discovery", ChannelStatus.UNAVAILABLE),
            _ch("hackernews", "signal", ChannelStatus.SUCCESS, 5),
        ]
        self.assertEqual(aggregate_run_status(results), RunStatus.CHANNEL_DOWN)

    def test_signal_down_with_healthy_discovery_is_partial(self):
        results = [
            _ch("arxiv", "discovery", ChannelStatus.SUCCESS, 1),
            _ch("openreview", "discovery", ChannelStatus.EMPTY),
            _ch("github", "discovery", ChannelStatus.SUCCESS, 1),
            _ch("hackernews", "signal", ChannelStatus.UNAVAILABLE),
            _ch("huggingface", "signal", ChannelStatus.SUCCESS, 2),
        ]
        self.assertEqual(aggregate_run_status(results), RunStatus.PARTIAL)

    def test_empty_is_not_unavailable_copy(self):
        empty_copy = status_reader_copy(ChannelStatus.EMPTY)
        down_copy = status_reader_copy(ChannelStatus.UNAVAILABLE)
        self.assertIn("无新命中", empty_copy)
        self.assertIn("不可用", down_copy)
        self.assertNotEqual(empty_copy, down_copy)
        self.assertIn("≠", down_copy)


if __name__ == "__main__":
    unittest.main()
