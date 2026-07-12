import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"

REQUIRED_FIELDS = {
    "id",
    "title",
    "authors",
    "date",
    "venue_or_source",
    "url",
    "relevance",
    "paper_type",
    "area",
    "why_included",
    "status",
}

VALID_RELEVANCE = {"core", "domain", "adjacent"}


def main() -> None:
    papers = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    if not isinstance(papers, list):
        raise SystemExit("data/papers.json must contain a list")

    seen_ids = set()
    for index, paper in enumerate(papers, start=1):
        missing = REQUIRED_FIELDS - paper.keys()
        if missing:
            raise SystemExit(f"paper #{index} missing fields: {sorted(missing)}")

        paper_id = paper["id"]
        if paper_id in seen_ids:
            raise SystemExit(f"duplicate id: {paper_id}")
        seen_ids.add(paper_id)

        if paper["relevance"] not in VALID_RELEVANCE:
            raise SystemExit(f"{paper_id}: invalid relevance {paper['relevance']!r}")

        if not paper["date"].startswith("2026-"):
            raise SystemExit(f"{paper_id}: date is outside the 2026+ window")

        if not paper["url"].startswith("https://"):
            raise SystemExit(f"{paper_id}: url must be https")

        authors = paper["authors"]
        if not isinstance(authors, list) or not authors:
            raise SystemExit(f"{paper_id}: authors must be a non-empty list")

    print(f"validated {len(papers)} papers")


if __name__ == "__main__":
    main()
