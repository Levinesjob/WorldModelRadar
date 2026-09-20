# WorldModel Radar

**秘书简报运行时** — 代你监督科技主线，不是 awesome list。  
Verified ledger（已核验清单）保持严格；讨论热度只提权分诊，永不单独决定收录。

**读者主入口：秘书日报/周报（Secretary Briefing）** → [`docs/digests/`](docs/digests/)

固定吸收顺序（限时可读）：

1. **今日/本周判断**（≤3 句）
2. **主线动态**（主线/长期，≤5）
3. **短期局部**（短期/局部优化，≤5，次要）
4. **热源雷达**（广覆盖·按分数优先 + 通道覆盖健康）
5. **缺口与下周盯梢**（≤5）
6. **管道健康**（紧凑）

每条核验 [Brief](data/briefs/) 必含：`claim` / `map_position` / `do` / `horizon`（`mainline`|`near_term`）/
`mainline_note` / `evidence_links`（`fake_demand` 可选）。主张中文优先。

**维护者入口：** [`docs/radar-runtime.md`](docs/radar-runtime.md) — 发现 → 分诊 → brief → 秘书周报。

```bash
# 离线（fixtures，无网络）— 热源 fixtures 独立于 papers.json
python3 -m radar run --fixtures
python3 -m unittest discover -s tests -v

# 在线（需网络；真实调用 HN Algolia + HF Daily Papers）
# 建议设置 GITHUB_TOKEN 以提高 GitHub 配额
python3 -m radar run
```

> **缩写首次展开：** HN = Hacker News（黑客新闻）；HF = Hugging Face Papers（每日论文）；
> VLA = Vision-Language-Action（视觉-语言-动作）。CLI 仍为 `radar`。

WorldModel Radar 跟踪 2026+ survey / roadmap / taxonomy / definition，以及 artifact 与
讨论信号，再压成 Brief 与秘书周报，服务建设者、研究者、架构与策略读者。

> Scope：优先收录以 world model / world modeling 为核心对象的 overview。
> 泛视频生成、AI agent 或具身综述仅在摘要把 world models 作为主对象时列为 adjacent。
> 热度可进分诊，不能单独进已核验清单。每条贡献必标 **主线/长期** vs **短期/局部**。

教义见 [`docs/radar-content-system.md`](docs/radar-content-system.md)；
核验门见 [`docs/inclusion-criteria.md`](docs/inclusion-criteria.md)。

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
|-- radar/                 # Radar Runtime / 秘书简报管道
|-- data/
|   |-- papers.json        # verified ledger seed
|   |-- clusters.json
|   |-- briefs/
|   |-- fixtures/          # offline adapter fixtures
|   `-- triage/
|-- docs/
|   |-- radar-runtime.md   # 如何跑 MVP
|   |-- digests/           # 秘书日报/周报（读者主入口）
|   |-- reviews/           # optional Deep Read HTML
|   `-- ...
|-- runs/                  # machine-readable run status
|-- scripts/               # legacy helpers (optional)
`-- tests/
```

## Data Fields

Canonical paper list: [`data/papers.json`](data/papers.json).

- `relevance`: `core`, `domain`, or `adjacent`
- `paper_type`: survey, review, roadmap, taxonomy, position, framework, etc.
- `area`: application or conceptual area
- `why_included`: short inclusion rationale
- `status`: `verified_public_source` when checked against public search/arXiv metadata

Brief 额外字段：`horizon` = `mainline`（主线/长期）| `near_term`（短期/局部）；
`mainline_note` = 一句中文说明对长期主线的影响（或明确「不改主线」）。

## Maintenance

```bash
python3 -m radar run --fixtures   # or: python3 -m radar run
python3 -m radar seed-briefs
python3 scripts/render_readme.py
python3 scripts/validate_papers.py
```

- Discovery（并行、失败隔离）：arXiv、OpenReview、GitHub。
- Optional heat（可降级）：Hacker News（HN）、Hugging Face Papers（HF）。
- 通道 `unavailable` ≠ 领域静默；热源不进「主线动态」栏。
- MVP **不**接 X / YouTube 自动热源。

详见 [`docs/radar-runtime.md`](docs/radar-runtime.md)、[`docs/automation.md`](docs/automation.md)。

## Deep Read (optional)

- [`docs/reviews/`](docs/reviews/)：长 HTML — 第二层，非每篇必写。
- [`docs/reviews/world-model-big-picture.html`](docs/reviews/world-model-big-picture.html)：遗留周合成。
