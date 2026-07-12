import json
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEWS_DIR = ROOT / "docs" / "reviews"
OUTPUT_FILE = REVIEWS_DIR / "reviews.json"


class ReviewMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "meta":
            return
        data = {key.lower(): value or "" for key, value in attrs}
        name = data.get("name", "")
        prefix = "worldmodel-radar:"
        if name.startswith(prefix):
            self.meta[name[len(prefix) :]] = data.get("content", "")


def parse_review(path: Path) -> dict | None:
    parser = ReviewMetaParser()
    parser.feed(path.read_text(encoding="utf-8"))
    if not parser.meta.get("paper-id"):
        return None
    relative_path = path.relative_to(ROOT).as_posix()
    return {
        "paper_id": parser.meta["paper-id"],
        "paper_title": parser.meta.get("paper-title", ""),
        "paper_url": parser.meta.get("paper-url", ""),
        "review_date": parser.meta.get("review-date", ""),
        "review_type": parser.meta.get("review-type", "deep_read"),
        "html_path": relative_path,
    }


def main() -> None:
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    reviews = []
    for path in sorted(REVIEWS_DIR.glob("*.html")):
        if path.name == "world-model-big-picture.html":
            continue
        parsed = parse_review(path)
        if parsed:
            reviews.append(parsed)

    reviews.sort(key=lambda item: (item["review_date"], item["paper_title"]), reverse=True)
    OUTPUT_FILE.write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(reviews)} reviews to {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
