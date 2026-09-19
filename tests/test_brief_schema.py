"""Brief schema validation tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from radar.brief import brief_from_paper, seed_briefs_from_papers, write_brief
from radar.paths import PAPERS_FILE
from radar.schemas import Brief, validate_brief


class BriefSchemaTests(unittest.TestCase):
    def test_valid_brief_passes(self):
        payload = {
            "claim": "若成立，评价协议从生成质量转向决策可采纳性。",
            "map_position": "eval · core · simulator assurance",
            "do": "研 — 跟评价合同与可审计指标",
            "fake_demand": "把演示视频当成可部署仿真",
            "evidence_links": ["https://arxiv.org/abs/2607.07196"],
        }
        self.assertEqual(validate_brief(payload), [])

    def test_missing_claim_fails(self):
        payload = {
            "map_position": "definition · core",
            "do": "观望 — 等共识",
            "evidence_links": ["https://arxiv.org/abs/x"],
        }
        errors = validate_brief(payload)
        self.assertTrue(any("claim" in e for e in errors))

    def test_empty_evidence_fails(self):
        payload = {
            "claim": "x",
            "map_position": "y",
            "do": "忽略 — z",
            "evidence_links": [],
        }
        errors = validate_brief(payload)
        self.assertTrue(any("evidence_links" in e for e in errors))

    def test_do_must_use_allowed_prefix(self):
        payload = {
            "claim": "x",
            "map_position": "y",
            "do": "买入 — 不对",
            "evidence_links": ["https://example.com"],
        }
        errors = validate_brief(payload)
        self.assertTrue(any("do must start" in e for e in errors))

    def test_claim_length_gate(self):
        payload = {
            "claim": "字" * 151,
            "map_position": "y",
            "do": "建 — ok",
            "evidence_links": ["https://example.com"],
        }
        errors = validate_brief(payload)
        self.assertTrue(any("≤150" in e for e in errors))

    def test_brief_from_paper_is_publishable(self):
        papers = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
        brief = brief_from_paper(papers[0])
        errors = validate_brief(brief.to_dict())
        self.assertEqual(errors, [], errors)

    def test_seed_all_papers(self):
        papers = json.loads(PAPERS_FILE.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            written, errors = seed_briefs_from_papers(papers, Path(tmp))
            self.assertEqual(errors, [])
            self.assertEqual(written, len(papers))
            self.assertEqual(len(list(Path(tmp).glob("*.json"))), len(papers))


if __name__ == "__main__":
    unittest.main()
