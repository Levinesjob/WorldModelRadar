import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "papers.json"
REVIEWS_FILE = ROOT / "docs" / "reviews" / "reviews.json"
OUTPUT_FILE = ROOT / "docs" / "reviews" / "world-model-big-picture.html"


def esc(value: object) -> str:
    text = "" if value is None else str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_json(path: Path, default: object) -> object:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def render_review_rows(reviews: list[dict], papers_by_id: dict[str, dict]) -> str:
    if not reviews:
        return "<tr><td colspan=\"5\">还没有精读 HTML。下一次日更会先生成第一篇。</td></tr>"

    rows = []
    for review in reviews:
        paper = papers_by_id.get(review["paper_id"], {})
        href = Path(review.get("html_path", "")).name
        rows.append(
            "<tr>"
            f"<td>{esc(review.get('review_date'))}</td>"
            f"<td><a href=\"{esc(href)}\">{esc(review.get('paper_title'))}</a></td>"
            f"<td>{esc(paper.get('relevance', ''))}</td>"
            f"<td>{esc(paper.get('area', ''))}</td>"
            f"<td><a href=\"{esc(review.get('paper_url'))}\">source</a></td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_area_rows(papers: list[dict], reviewed_ids: set[str]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for paper in papers:
        grouped[paper.get("area", "unknown")].append(paper)

    rows = []
    for area, area_papers in sorted(grouped.items(), key=lambda item: (-len(item[1]), item[0])):
        reviewed = sum(1 for paper in area_papers if paper["id"] in reviewed_ids)
        relevance = Counter(paper["relevance"] for paper in area_papers)
        rows.append(
            "<tr>"
            f"<td>{esc(area)}</td>"
            f"<td>{len(area_papers)}</td>"
            f"<td>{reviewed}</td>"
            f"<td>{relevance.get('core', 0)} core / {relevance.get('domain', 0)} domain / {relevance.get('adjacent', 0)} adjacent</td>"
            "</tr>"
        )
    return "\n".join(rows)


def render_priority_list(papers: list[dict], reviewed_ids: set[str]) -> str:
    unreviewed = [paper for paper in papers if paper["id"] not in reviewed_ids]
    if not unreviewed:
        return "<li>当前主表论文都已有精读 HTML，下一步应更新跨论文综合判断。</li>"

    priority = {"core": 3, "domain": 2, "adjacent": 1}
    unreviewed.sort(
        key=lambda paper: (
            priority.get(paper.get("relevance"), 0),
            paper.get("date", ""),
            paper.get("title", ""),
        ),
        reverse=True,
    )
    return "\n".join(
        f"<li><strong>{esc(paper['title'])}</strong><span>{esc(paper['area'])} · {esc(paper['date'])}</span></li>"
        for paper in unreviewed[:6]
    )


def main() -> None:
    papers = load_json(DATA_FILE, [])
    reviews = load_json(REVIEWS_FILE, [])
    papers_by_id = {paper["id"]: paper for paper in papers}
    reviewed_ids = {review["paper_id"] for review in reviews}
    counts = Counter(paper["relevance"] for paper in papers)
    today = date.today().isoformat()

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WorldModel Radar | Big Picture</title>
  <style>
    :root {{
      --ink: #15201b;
      --muted: #5d6a63;
      --paper: #f7f2e8;
      --panel: #fffaf1;
      --line: #d8cdb8;
      --green: #1d7a61;
      --blue: #235d86;
      --red: #af4538;
      --amber: #b9831e;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--paper);
      font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif;
      line-height: 1.55;
    }}
    a {{ color: var(--blue); }}
    header, section, footer {{ padding: 40px clamp(20px, 5vw, 72px); border-bottom: 1px solid var(--line); }}
    .wrap {{ max-width: 1240px; margin: 0 auto; }}
    .kicker {{ font: 12px/1.2 "Trebuchet MS", Verdana, sans-serif; text-transform: uppercase; color: var(--muted); letter-spacing: 0; }}
    h1 {{ max-width: 980px; margin: 8px 0 18px; font-size: 72px; line-height: 0.96; letter-spacing: 0; }}
    h2 {{ margin: 0 0 16px; font-size: 36px; line-height: 1; letter-spacing: 0; }}
    .lead {{ max-width: 860px; font-size: 22px; color: #33423a; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 28px; }}
    .metric {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 18px; }}
    .metric strong {{ display: block; font-size: 34px; line-height: 1; }}
    .metric span {{ color: var(--muted); font: 13px/1.4 "Trebuchet MS", Verdana, sans-serif; }}
    .map {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 18px; }}
    .panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 22px; }}
    .axes {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .axis {{ border-top: 5px solid var(--green); padding-top: 12px; }}
    .axis:nth-child(2) {{ border-color: var(--blue); }}
    .axis:nth-child(3) {{ border-color: var(--red); }}
    .axis:nth-child(4) {{ border-color: var(--amber); }}
    table {{ width: 100%; border-collapse: collapse; background: var(--panel); border: 1px solid var(--line); }}
    th, td {{ padding: 12px 14px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ font: 12px/1.2 "Trebuchet MS", Verdana, sans-serif; text-transform: uppercase; color: var(--muted); letter-spacing: 0; }}
    .priority {{ display: grid; gap: 10px; margin: 0; padding: 0; list-style: none; }}
    .priority li {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }}
    .priority span {{ display: block; color: var(--muted); margin-top: 4px; font-size: 14px; }}
    footer {{ color: var(--muted); font: 13px/1.5 "Trebuchet MS", Verdana, sans-serif; }}
    @media (max-width: 860px) {{
      h1 {{ font-size: 48px; }}
      .metrics, .map, .axes {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 520px) {{
      h1 {{ font-size: 36px; }}
      .lead {{ font-size: 18px; }}
      th, td {{ padding: 10px 8px; font-size: 14px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <p class="kicker">WorldModel Radar · Weekly Big Picture · {today}</p>
      <h1>世界模型大图景</h1>
      <p class="lead">这份页面把已经生成的精读 HTML 汇总成一张持续更新的研究地图：哪些论文定义问题，哪些论文打开应用场景，哪些地方还缺少真实评估和可迁移架构。</p>
      <div class="metrics">
        <div class="metric"><strong>{len(papers)}</strong><span>papers in radar</span></div>
        <div class="metric"><strong>{len(reviews)}</strong><span>deep-read HTML reviews</span></div>
        <div class="metric"><strong>{counts.get('core', 0)}</strong><span>core world-model papers</span></div>
        <div class="metric"><strong>{len(papers) - len(reviewed_ids)}</strong><span>papers still to review</span></div>
      </div>
    </div>
  </header>

  <section>
    <div class="wrap map">
      <div class="panel">
        <h2>战略坐标</h2>
        <div class="axes">
          <div class="axis"><strong>定义层</strong><p>统一概念、能力边界、分类法和路线图，是后续所有论文比较的坐标系。</p></div>
          <div class="axis"><strong>交互层</strong><p>从视频生成走向可行动模拟，关键问题是动作、状态、反馈和长时序一致性。</p></div>
          <div class="axis"><strong>领域层</strong><p>机器人、医疗、边缘智能、代码智能会先落地，因为它们有明确场景、成本约束和评价指标。</p></div>
          <div class="axis"><strong>工程层</strong><p>真正的壁垒来自数据闭环、评估体系、推理成本、安全边界和迁移路径，而不只是单个模型。</p></div>
        </div>
      </div>
      <div class="panel">
        <h2>下一批精读优先级</h2>
        <ul class="priority">
          {render_priority_list(papers, reviewed_ids)}
        </ul>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>已完成精读</h2>
      <table>
        <thead><tr><th>Date</th><th>Review</th><th>Relevance</th><th>Area</th><th>Source</th></tr></thead>
        <tbody>
          {render_review_rows(reviews, papers_by_id)}
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>覆盖矩阵</h2>
      <table>
        <thead><tr><th>Area</th><th>Papers</th><th>Reviewed</th><th>Mix</th></tr></thead>
        <tbody>
          {render_area_rows(papers, reviewed_ids)}
        </tbody>
      </table>
    </div>
  </section>

  <footer>
    <div class="wrap">Generated from data/papers.json and docs/reviews/reviews.json. Weekly automation should refine this page with cross-paper synthesis when more reviews are available.</div>
  </footer>
</body>
</html>
"""
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"wrote {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
