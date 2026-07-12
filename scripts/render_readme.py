import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README_FILE = ROOT / "README.md"
DATA_FILE = ROOT / "data" / "papers.json"

START_MARKER = "<!-- QUICK_VIEW:START -->"
END_MARKER = "<!-- QUICK_VIEW:END -->"


def escape_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_quick_view(papers: list[dict]) -> str:
    counts = Counter(paper["relevance"] for paper in papers)
    sorted_papers = sorted(
        papers,
        key=lambda paper: (paper["date"], paper["title"].lower()),
        reverse=True,
    )

    lines = [
        START_MARKER,
        "",
        f"截至 {date.today().isoformat()}，本仓库记录了 {len(papers)} 篇 2026 年以来的公开可检索论文，其中：",
        "",
        f"- {counts['core']} 篇 core：直接综述、定义、路线图或 taxonomy 世界模型本体。",
        f"- {counts['domain']} 篇 domain：围绕机器人、医疗、边缘智能、代码智能等领域中的世界模型。",
        f"- {counts['adjacent']} 篇 adjacent：与世界模型强相关，但主对象更偏泛世界模型相邻主题。",
        "",
        "| Date | Relevance | Area | Paper |",
        "| --- | --- | --- | --- |",
    ]

    for paper in sorted_papers:
        title = escape_cell(paper["title"])
        area = escape_cell(paper["area"])
        lines.append(
            f"| {paper['date']} | {paper['relevance']} | {area} | [{title}]({paper['url']}) |"
        )

    lines.extend(["", END_MARKER])
    return "\n".join(lines)


def main() -> None:
    readme = README_FILE.read_text(encoding="utf-8")
    papers = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    quick_view = render_quick_view(papers)

    if START_MARKER not in readme or END_MARKER not in readme:
        raise SystemExit("README.md is missing quick-view markers")

    before, rest = readme.split(START_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)
    README_FILE.write_text(before + quick_view + after, encoding="utf-8")
    print(f"rendered README quick view for {len(papers)} papers")


if __name__ == "__main__":
    main()
