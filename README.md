# WorldModel Radar

Intelligence map for world models — **not** an awesome list. Content first;
verified ledger stays strict; discussion heat raises priority only and never
decides inclusion alone.

**Reader entry:** start from the [Weekly Digest](docs/digests/)（本周可带走的结论 →
地图与缺口 → 本周信号 → 核验 Brief → 管道健康）. Each verified item has a
short Chinese [Brief](data/briefs/) (`claim` / `map_position` / `do` /
`fake_demand` / `evidence_links`). Optional HTML deep reads remain under
`docs/reviews/`.

**Maintainer entry:** [`docs/radar-runtime.md`](docs/radar-runtime.md) — run
discovery → triage → brief → digest in a clean environment in ~30 minutes.

```bash
# Offline (fixtures, no network) — heat fixtures are distinct from papers.json
python3 -m radar run --fixtures
python3 -m unittest discover -s tests -v

# Live (needs network; actually calls HN Algolia + HF Daily Papers)
# set GITHUB_TOKEN for better GitHub quota
python3 -m radar run
```

WorldModel Radar tracks 2026+ survey, roadmap, taxonomy, and definition papers,
plus artifact and discussion signals, then turns them into Briefs and weekly
synthesis for builders, researchers, architects, and strategy readers.

> Scope note: 优先收录标题、摘要或正文明确以 world model / world modeling /
> world modelling 为核心对象的 overview 类工作。泛视频生成、AI agent 或具身智能
> 综述只有在摘要把 world models 作为主要讨论对象时才列为 adjacent。热度信号可进
> 分诊队列，但不能单独进入已核验清单。

See [`docs/radar-content-system.md`](docs/radar-content-system.md) for the
editorial system and [`docs/inclusion-criteria.md`](docs/inclusion-criteria.md)
for the verified-ledger gate.

## Quick View

<!-- QUICK_VIEW:START -->

截至 2026-09-07，本仓库记录了 19 篇 2026 年以来的公开可检索论文，其中：

- 11 篇 core：直接综述、定义、路线图或 taxonomy 世界模型本体。
- 7 篇 domain：围绕机器人、医疗、边缘智能、代码智能等领域中的世界模型。
- 1 篇 adjacent：与世界模型强相关，但主对象更偏泛世界模型相邻主题。

| Date | Relevance | Area | Paper |
| --- | --- | --- | --- |
| 2026-08-12 | domain | driving world models and counterfactual evaluation | [How Can Driving World Models Do Counterfactual Prediction?](https://arxiv.org/abs/2608.11601) |
| 2026-08-06 | domain | economic world models | [From Economic Agents to Agentic Economies: A Systems Blueprint for Economic World Models](https://arxiv.org/abs/2608.06020) |
| 2026-07-13 | core | world action models and embodied physical intelligence | [From World Action Models to Embodied Brains: A Roadmap for Open-World Physical Intelligence](https://arxiv.org/abs/2607.11689) |
| 2026-07-08 | core | world-model simulator assurance | [Validate the Dream Before You Trust Its Verdict: Admissibility for World-Model Simulators](https://arxiv.org/abs/2607.07196) |
| 2026-07-07 | core | general definition | [A Definition and Roadmap for World Models](https://arxiv.org/abs/2607.06401) |
| 2026-06-15 | domain | healthcare | [Medical world models: representing medical states, modelling clinical dynamics and guiding intervention policies](https://arxiv.org/abs/2606.16721) |
| 2026-06-13 | core | decision-centric world-model evaluation | [How Should World Models Be Evaluated for Embodied Decision-Making? A Decision-Making-Centric Position](https://arxiv.org/abs/2606.15032) |
| 2026-06-04 | domain | robotics, VLA, and world-model interfaces | [Robots Need More than VLA and World Models](https://arxiv.org/abs/2606.06556) |
| 2026-05-31 | core | interactive video world modeling | [Towards Interactive Video World Modeling: Frontiers, Challenges, Benchmarks, and Future Trends](https://arxiv.org/abs/2606.01164) |
| 2026-05-12 | core | embodied AI and action generation | [World Action Models: The Next Frontier in Embodied AI](https://arxiv.org/abs/2605.12090) |
| 2026-04-30 | core | robot learning | [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) |
| 2026-04-30 | core | graph world models | [Graph World Models: Concepts, Taxonomy, and Future Directions](https://arxiv.org/abs/2604.27895) |
| 2026-04-09 | domain | code intelligence | [Beyond the Autoregressive Horizon: A Comprehensive Survey of Diffusion Models, World Modelling, and State Space Models for Code](https://arxiv.org/abs/2606.23690) |
| 2026-04-07 | adjacent | video generation foundations | [Evolution of Video Generative Foundations](https://arxiv.org/abs/2604.06339) |
| 2026-04-06 | core | advanced world models | [OpenWorldLib: A Unified Codebase and Definition of Advanced World Models](https://arxiv.org/abs/2604.04707) |
| 2026-03-18 | domain | digital twins and mobile edge intelligence | [From Digital Twins to World Models: Opportunities, Challenges, and Applications for Mobile Edge General Intelligence](https://arxiv.org/abs/2603.17420) |
| 2026-02-02 | core | world-model research framing | [Research on World Models Is Not Merely Injecting World Knowledge into Specific Tasks](https://arxiv.org/abs/2602.01630) |
| 2026-01-21 | core | physical grounding and actionable simulators | [From Generative Engines to Actionable Simulators: The Imperative of Physical Grounding in World Models](https://arxiv.org/abs/2601.15533) |
| 2026-01-12 | domain | robotics and video generation world models | [Video Generation Models in Robotics - Applications, Research Challenges, Future Directions](https://arxiv.org/abs/2601.07823) |

<!-- QUICK_VIEW:END -->

## Repository Layout

```text
.
|-- README.md
|-- radar/                 # Radar Runtime (default path)
|-- data/
|   |-- papers.json        # verified ledger seed
|   |-- clusters.json
|   |-- briefs/
|   |-- fixtures/          # offline adapter fixtures
|   `-- triage/
|-- docs/
|   |-- radar-runtime.md   # how to run the MVP pipeline
|   |-- digests/           # Weekly Digest (primary reader entry)
|   |-- reviews/           # optional Deep Read HTML
|   `-- ...
|-- runs/                  # machine-readable run status
|-- scripts/               # legacy helpers (optional)
`-- tests/
```

## Data Fields

The canonical paper list lives in [`data/papers.json`](data/papers.json).

- `relevance`: `core`, `domain`, or `adjacent`
- `paper_type`: survey, review, roadmap, taxonomy, position, framework, etc.
- `area`: the application or conceptual area
- `why_included`: short inclusion rationale
- `status`: `verified_public_source` when checked against public search/arXiv metadata

## Maintenance

Default pipeline (multi-channel, isolated adapters):

```bash
python3 -m radar run --fixtures   # or: python3 -m radar run
python3 -m radar seed-briefs
python3 scripts/render_readme.py
python3 scripts/validate_papers.py
```

- Discovery channels (parallel, failure-isolated): arXiv, OpenReview, GitHub.
- Optional signal channels (degradable): Hacker News, Hugging Face Papers.
- Channel `unavailable` ≠ empty field; never narrate outages as “zero candidates”.
- Move weak hits to triage / `docs/search-log.md`; only primary-source-verified
  overview items enter `data/papers.json`.

See [`docs/radar-runtime.md`](docs/radar-runtime.md) and legacy notes in
[`docs/automation.md`](docs/automation.md).

## Deep Read (optional)

- [`docs/reviews/`](docs/reviews/): long HTML reviews — second layer, not required
  for every paper.
- [`docs/reviews/world-model-big-picture.html`](docs/reviews/world-model-big-picture.html):
  legacy weekly synthesis over the HTML corpus.
