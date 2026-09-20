"""Shared path helpers for the Radar Runtime."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
PAPERS_FILE = DATA_DIR / "papers.json"
CLUSTERS_FILE = DATA_DIR / "clusters.json"
BRIEFS_DIR = DATA_DIR / "briefs"
TRIAGE_DIR = DATA_DIR / "triage"
FIXTURES_DIR = DATA_DIR / "fixtures"
RUNS_DIR = ROOT / "runs"
DIGESTS_DIR = ROOT / "docs" / "digests"
