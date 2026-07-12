import argparse
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
DEFAULT_OUTPUT = ROOT / "data" / "candidates" / "latest.json"

ARXIV_API = "https://export.arxiv.org/api/query"
START_DATE = date(2026, 1, 1)
ATOM = {"atom": "http://www.w3.org/2005/Atom"}

QUERIES = [
    'all:world AND all:model AND (all:survey OR all:review OR all:roadmap OR all:taxonomy OR all:definition OR all:framework OR all:position)',
    'all:world AND all:models AND (all:survey OR all:review OR all:roadmap OR all:taxonomy OR all:definition OR all:framework OR all:position)',
    'all:world AND all:modeling AND (all:survey OR all:review OR all:roadmap OR all:taxonomy OR all:definition OR all:framework OR all:position)',
    'all:world AND all:modelling AND (all:survey OR all:review OR all:roadmap OR all:taxonomy OR all:definition OR all:framework OR all:position)',
]

WORLD_RE = re.compile(r"\bworld\s+model(s|ing|ling)?\b", re.IGNORECASE)
OVERVIEW_RE = re.compile(
    r"\b(survey|review|roadmap|taxonomy|definition|framework|position|critique|"
    r"future directions?|challenges?|benchmarks?|opportunit(?:y|ies))\b",
    re.IGNORECASE,
)


def load_known_ids() -> set[str]:
    papers = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {paper.get("arxiv_id", "") for paper in papers if paper.get("arxiv_id")}


def arxiv_id_from_url(url: str) -> str:
    raw_id = url.rstrip("/").rsplit("/", 1)[-1]
    return re.sub(r"v\d+$", "", raw_id)


def fetch_query(query: str, max_results: int) -> list[dict]:
    params = {
        "search_query": query,
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as response:
        xml_text = response.read()

    root = ET.fromstring(xml_text)
    results = []
    for entry in root.findall("atom:entry", ATOM):
        entry_url = entry.findtext("atom:id", default="", namespaces=ATOM)
        published = entry.findtext("atom:published", default="", namespaces=ATOM)[:10]
        if not published:
            continue
        if date.fromisoformat(published) < START_DATE:
            continue

        title = " ".join(entry.findtext("atom:title", default="", namespaces=ATOM).split())
        summary = " ".join(entry.findtext("atom:summary", default="", namespaces=ATOM).split())
        authors = [
            author.findtext("atom:name", default="", namespaces=ATOM)
            for author in entry.findall("atom:author", ATOM)
        ]
        text = f"{title}\n{summary}"
        if not WORLD_RE.search(text) or not OVERVIEW_RE.search(text):
            continue

        results.append(
            {
                "arxiv_id": arxiv_id_from_url(entry_url),
                "title": title,
                "authors": [author for author in authors if author],
                "published": published,
                "updated": entry.findtext("atom:updated", default="", namespaces=ATOM)[:10],
                "url": entry_url,
                "summary": summary,
                "matched_query": query,
            }
        )
    return results


def discover(max_results: int) -> list[dict]:
    known_ids = load_known_ids()
    candidates_by_id: dict[str, dict] = {}
    for query in QUERIES:
        for candidate in fetch_query(query, max_results):
            arxiv_id = candidate["arxiv_id"]
            if arxiv_id in known_ids:
                continue
            if arxiv_id not in candidates_by_id:
                candidate["matched_queries"] = [candidate.pop("matched_query")]
                candidates_by_id[arxiv_id] = candidate
            else:
                candidates_by_id[arxiv_id]["matched_queries"].append(candidate["matched_query"])

    return sorted(
        candidates_by_id.values(),
        key=lambda candidate: (candidate["published"], candidate["title"].lower()),
        reverse=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Find new arXiv world-model overview candidates.")
    parser.add_argument("--max-results", type=int, default=50)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--print-only", action="store_true")
    args = parser.parse_args()

    candidates = discover(args.max_results)
    payload = {
        "source": "arXiv",
        "start_date": START_DATE.isoformat(),
        "candidate_count": len(candidates),
        "candidates": candidates,
    }

    if args.print_only:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(candidates)} candidates to {args.output}")


if __name__ == "__main__":
    main()
