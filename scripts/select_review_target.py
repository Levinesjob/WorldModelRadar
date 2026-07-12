import argparse
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
REVIEWS_FILE = ROOT / "docs" / "reviews" / "reviews.json"


RELEVANCE_WEIGHT = {
    "core": 100,
    "domain": 70,
    "adjacent": 35,
}

TYPE_KEYWORDS = {
    "definition": 28,
    "roadmap": 26,
    "taxonomy": 24,
    "survey": 22,
    "review": 22,
    "framework": 18,
    "position": 16,
    "benchmark": 12,
}

AREA_WEIGHT = {
    "general definition": 20,
    "advanced world models": 16,
    "interactive video world modeling": 14,
    "robot learning": 12,
    "embodied AI and action generation": 12,
    "physical grounding and actionable simulators": 12,
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "world-model-review"


def load_papers() -> list[dict]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def load_reviewed_ids() -> set[str]:
    if not REVIEWS_FILE.exists():
        return set()
    reviews = json.loads(REVIEWS_FILE.read_text(encoding="utf-8"))
    return {review["paper_id"] for review in reviews if review.get("paper_id")}


def score_paper(paper: dict) -> int:
    score = RELEVANCE_WEIGHT.get(paper.get("relevance"), 0)
    paper_type = paper.get("paper_type", "").lower()
    for keyword, weight in TYPE_KEYWORDS.items():
        if keyword in paper_type:
            score += weight

    area = paper.get("area", "")
    score += AREA_WEIGHT.get(area, 0)

    title = paper.get("title", "").lower()
    if "world model" in title or "world models" in title:
        score += 8
    if "comprehensive" in title:
        score += 5
    return score


def suggested_html_path(paper: dict) -> str:
    slug = slugify(paper["title"])
    return f"docs/reviews/{slug}.html"


def choose_paper(
    papers: list[dict],
    reviewed_ids: set[str],
    prefer_ids: set[str],
    prefer_date: str | None,
) -> tuple[dict, str]:
    def best(candidates: list[dict]) -> dict | None:
        if not candidates:
            return None
        return max(
            candidates,
            key=lambda paper: (
                score_paper(paper),
                paper.get("date", ""),
                paper.get("title", ""),
            ),
        )

    if prefer_ids:
        preferred = [
            paper
            for paper in papers
            if paper.get("id") in prefer_ids or paper.get("arxiv_id") in prefer_ids
        ]
        selected = best(preferred)
        if selected:
            return selected, "highest_value_from_today_updates"

    if prefer_date:
        same_date = [paper for paper in papers if paper.get("date") == prefer_date]
        selected = best(same_date)
        if selected:
            return selected, "highest_value_from_preferred_date"

    unreviewed = [paper for paper in papers if paper.get("id") not in reviewed_ids]
    selected = best(unreviewed)
    if selected:
        return selected, "highest_value_unreviewed_existing_paper"

    selected = best(papers)
    if selected:
        return selected, "all_papers_reviewed_refresh_highest_value_paper"

    raise SystemExit("No papers available in data/papers.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Select the next paper for deep HTML review.")
    parser.add_argument(
        "--prefer-id",
        action="append",
        default=[],
        help="Prefer a newly added paper id or arXiv id. Can be repeated.",
    )
    parser.add_argument(
        "--prefer-date",
        default=None,
        help="Prefer papers with this publication date, formatted as YYYY-MM-DD.",
    )
    parser.add_argument("--today", action="store_true", help="Prefer papers dated today.")
    args = parser.parse_args()

    prefer_date = date.today().isoformat() if args.today else args.prefer_date
    papers = load_papers()
    reviewed_ids = load_reviewed_ids()
    selected, reason = choose_paper(papers, reviewed_ids, set(args.prefer_id), prefer_date)

    output = {
        "selected_at": date.today().isoformat(),
        "reason": reason,
        "score": score_paper(selected),
        "already_reviewed": selected["id"] in reviewed_ids,
        "suggested_html_path": suggested_html_path(selected),
        "paper": selected,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
