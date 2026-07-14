import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


finder = load_script("find_arxiv_candidates")
selector = load_script("select_review_target")


class DiscoveryConfidenceTests(unittest.TestCase):
    def test_world_action_model_roadmap_is_high_confidence_discovery(self):
        confidence, evidence = finder.assess_discovery_confidence(
            "From World Action Models to Embodied Brains: A Roadmap",
            "We review the evolution and propose a roadmap.",
        )
        self.assertEqual(confidence, "high")
        self.assertIn("world-model phrase appears in title", evidence)

    def test_single_method_world_model_paper_is_not_high_confidence_discovery(self):
        confidence, _ = finder.assess_discovery_confidence(
            "Causally Debiased Latent Action Model for World Models",
            "We propose a framework for fine-tuning.",
        )
        self.assertEqual(confidence, "medium")


class SelectionConfidenceTests(unittest.TestCase):
    def setUp(self):
        self.paper = {
            "id": "example-2026-world-model-roadmap",
            "title": "A Roadmap for World Models",
            "authors": ["A. Researcher"],
            "date": "2026-07-14",
            "venue_or_source": "arXiv",
            "arxiv_id": "2607.00001",
            "url": "https://arxiv.org/abs/2607.00001",
            "relevance": "core",
            "paper_type": "review/roadmap",
            "why_included": "Reviews the field and proposes a roadmap.",
            "status": "verified_public_source",
        }

    def test_verified_canonical_overview_is_eligible(self):
        self.assertTrue(selector.is_high_confidence_paper(self.paper))

    def test_noncanonical_url_is_ineligible(self):
        self.paper["url"] = "https://example.com/paper"
        self.assertFalse(selector.is_high_confidence_paper(self.paper))

    def test_single_method_type_is_ineligible(self):
        self.paper["paper_type"] = "method"
        self.assertFalse(selector.is_high_confidence_paper(self.paper))


if __name__ == "__main__":
    unittest.main()
