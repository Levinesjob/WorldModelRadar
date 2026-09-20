"""Brief schema validation tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from radar.brief import brief_from_paper, seed_briefs_from_papers
from radar.paths import PAPERS_FILE
from radar.schemas import Horizon, validate_brief


class BriefSchemaTests(unittest.TestCase):
    def test_valid_brief_passes(self):
        payload = {
            "claim": "若成立，评价协议从生成质量转向决策可采纳性。",
            "map_position": "eval · core · simulator assurance",
            "do": "研 — 跟评价合同与可审计指标",
            "fake_demand": "把演示视频当成可部署仿真",
            "evidence_links": ["https://arxiv.org/abs/2607.07196"],
            "horizon": "mainline",
            "mainline_note": "把评价主线从生成质量扭向决策可采纳性。",
        }
        self.assertEqual(validate_brief(payload), [])

    def test_missing_claim_fails(self):
        payload = {
            "map_position": "definition · core",
            "do": "观望 — 等共识",
            "evidence_links": ["https://arxiv.org/abs/x"],
            "horizon": "mainline",
            "mainline_note": "触及定义。",
        }
        errors = validate_brief(payload)
        self.assertTrue(any("claim" in e for e in errors))

    def test_missing_horizon_fails(self):
        payload = {
            "claim": "x",
            "map_position": "y",
            "do": "研 — z",
            "evidence_links": ["https://example.com"],
            "mainline_note": "note",
        }
        errors = validate_brief(payload)
        self.assertTrue(any("horizon" in e for e in errors))

    def test_missing_mainline_note_fails(self):
        payload = {
            "claim": "x",
            "map_position": "y",
            "do": "研 — z",
            "evidence_links": ["https://example.com"],
            "horizon": "near_term",
        }
        errors = validate_brief(payload)
        self.assertTrue(any("mainline_note" in e for e in errors))

    def test_invalid_horizon_fails(self):
        payload = {
            "claim": "x",
            "map_position": "y",
            "do": "研 — z",
            "evidence_links": ["https://example.com"],
            "horizon": "forever",
            "mainline_note": "n",
        }
        errors = validate_brief(payload)
        self.assertTrue(any("horizon" in e for e in errors))

    def test_empty_evidence_fails(self):
        payload = {
            "claim": "x",
            "map_position": "y",
            "do": "忽略 — z",
            "evidence_links": [],
            "horizon": "near_term",
            "mainline_note": "局部。",
        }
        errors = validate_brief(payload)
        self.assertTrue(any("evidence_links" in e for e in errors))

    def test_do_must_use_allowed_prefix(self):
        payload = {
            "claim": "x",
            "map_position": "y",
            "do": "买入 — 不对",
            "evidence_links": ["https://example.com"],
            "horizon": "near_term",
            "mainline_note": "n",
        }
        errors = validate_brief(payload)
        self.assertTrue(any("do must start" in e for e in errors))

    def test_claim_length_gate(self):
        payload = {
            "claim": "字" * 151,
            "map_position": "y",
            "do": "建 — ok",
            "evidence_links": ["https://example.com"],
            "horizon": "mainline",
            "mainline_note": "n",
        }
        errors = validate_brief(payload)
        self.assertTrue(any("≤150" in e for e in errors))

    def test_brief_from_paper_is_publishable(self):
        papers = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
        brief = brief_from_paper(papers[0])
        payload = brief.to_dict()
        errors = validate_brief(payload)
        self.assertEqual(errors, [], errors)
        self.assertIn(payload["horizon"], (Horizon.MAINLINE.value, Horizon.NEAR_TERM.value))
        self.assertTrue(payload["mainline_note"].strip())

    def test_seed_all_papers_have_horizon(self):
        papers = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            written, errors = seed_briefs_from_papers(papers, Path(tmp))
            self.assertEqual(errors, [])
            self.assertEqual(written, len(papers))
            for path in Path(tmp).glob("*.json"):
                data = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn(data["horizon"], ("mainline", "near_term"))
                self.assertTrue(data["mainline_note"].strip())

    def test_definition_roadmap_is_mainline(self):
        papers = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
        paper = next(p for p in papers if p["id"] == "chen-2026-definition-roadmap-world-models")
        brief = brief_from_paper(paper)
        self.assertEqual(brief.horizon, "mainline")
        self.assertIn("定义", brief.mainline_note)

    def test_adjacent_video_is_near_term(self):
        papers = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
        paper = next(p for p in papers if p["id"] == "hu-2026-evolution-video-generative-foundations")
        brief = brief_from_paper(paper)
        self.assertEqual(brief.horizon, "near_term")


if __name__ == "__main__":
    unittest.main()
