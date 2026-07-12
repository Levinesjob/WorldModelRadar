# WorldModel Radar

Tracking 2026+ survey, roadmap, taxonomy, and definition papers on world models.

这是一个面向“世界模型（World Models）”综述论文的轻量仓库，收录范围从
2026-01-01 到 2026-07-12。

> Scope note: 本仓库优先收录标题、摘要或正文明确以 world model/world
> modeling/world modelling 为核心对象的 survey、review、roadmap、taxonomy、
> position 或 definition/framework 类论文。泛视频生成、AI agent 或具身智能综述
> 只有在摘要明确把 world models 作为主要讨论对象时才列为 adjacent。

## Quick View

截至 2026-07-12，本仓库记录了 14 篇 2026 年以来的公开可检索论文，其中：

- 8 篇 core：直接综述、定义、路线图或 taxonomy 世界模型本体。
- 5 篇 domain：围绕机器人、医疗、边缘智能、代码智能等领域中的世界模型。
- 1 篇 adjacent：与世界模型强相关，但主对象更偏视频生成基础模型。

| Date | Relevance | Area | Paper |
| --- | --- | --- | --- |
| 2026-07-07 | core | general definition | [A Definition and Roadmap for World Models](https://arxiv.org/abs/2607.06401) |
| 2026-06-15 | domain | healthcare | [Medical world models: representing medical states, modelling clinical dynamics and guiding intervention policies](https://arxiv.org/abs/2606.16721) |
| 2026-06-04 | domain | robotics | [Robots Need More than VLA and World Models](https://arxiv.org/abs/2606.06556) |
| 2026-05-31 | core | interactive video | [Towards Interactive Video World Modeling: Frontiers, Challenges, Benchmarks, and Future Trends](https://arxiv.org/abs/2606.01164) |
| 2026-05-12 | core | embodied AI | [World Action Models: The Next Frontier in Embodied AI](https://arxiv.org/abs/2605.12090) |
| 2026-04-30 | core | robot learning | [World Model for Robot Learning: A Comprehensive Survey](https://arxiv.org/abs/2605.00080) |
| 2026-04-30 | core | graph world models | [Graph World Models: Concepts, Taxonomy, and Future Directions](https://arxiv.org/abs/2604.27895) |
| 2026-04-09 | domain | code intelligence | [Beyond the Autoregressive Horizon: A Comprehensive Survey of Diffusion Models, World Modelling, and State Space Models for Code](https://arxiv.org/abs/2606.23690) |
| 2026-04-07 | adjacent | video generation | [Evolution of Video Generative Foundations](https://arxiv.org/abs/2604.06339) |
| 2026-04-06 | core | framework/definition | [OpenWorldLib: A Unified Codebase and Definition of Advanced World Models](https://arxiv.org/abs/2604.04707) |
| 2026-03-18 | domain | digital twins / edge AI | [From Digital Twins to World Models: Opportunities, Challenges, and Applications for Mobile Edge General Intelligence](https://arxiv.org/abs/2603.17420) |
| 2026-02-02 | core | research framing | [Research on World Models Is Not Merely Injecting World Knowledge into Specific Tasks](https://arxiv.org/abs/2602.01630) |
| 2026-01-21 | core | physical grounding | [From Generative Engines to Actionable Simulators: The Imperative of Physical Grounding in World Models](https://arxiv.org/abs/2601.15533) |
| 2026-01-12 | domain | robotics / video models | [Video Generation Models in Robotics - Applications, Research Challenges, Future Directions](https://arxiv.org/abs/2601.07823) |

## Repository Layout

```text
.
├── README.md
├── data/
│   └── papers.json
├── docs/
│   ├── inclusion-criteria.md
│   └── search-log.md
└── scripts/
    └── validate_papers.py
```

## Data Fields

The canonical paper list lives in [`data/papers.json`](data/papers.json).

- `relevance`: `core`, `domain`, or `adjacent`
- `paper_type`: survey, review, roadmap, taxonomy, position, framework, etc.
- `area`: the application or conceptual area
- `why_included`: short inclusion rationale
- `status`: `verified_public_source` when checked against public search/arXiv metadata

## Maintenance

Run the validator after editing metadata:

```bash
python scripts/validate_papers.py
```

Suggested update cadence:

- Search monthly for new arXiv papers containing `world model`, `world models`,
  `world modeling`, and `world modelling`.
- Add newly found 2026+ papers only if they satisfy the inclusion criteria.
- Move broad-but-weak hits into `docs/search-log.md` instead of forcing them into
  the canonical list.
