# Radar Runtime — 秘书简报 30 分钟跑通指南

目标：在干净环境完成 **发现 → 分诊 → Brief → 秘书日报/周报（Secretary Briefing）**，并看懂 run status。  
CLI 仍为 `python -m radar`；读者主入口文案为 **秘书周报**，不是信息倾销。

## 前置

- Python 3.10+（仅标准库；无需 pip）
- 克隆本仓库并进入根目录

```bash
git clone https://github.com/Levinesjob/WorldModelRadar.git
cd WorldModelRadar
```

## 离线全流程（推荐先跑，~2 分钟）

使用 `data/fixtures/`，**不访问网络**：

```bash
python -m radar run --fixtures
python -m unittest discover -s tests -v
```

`--fixtures` 会：

1. 从 `data/papers.json`（已核验清单 / ledger）生成核验 Brief（含 `horizon` + `mainline_note`）；
2. 用离线 fixtures 跑发现 + 热源适配器（arXiv / OpenReview / GitHub / HN / HF Papers）；
3. 写出分诊队列、**秘书周报**、run status。

热源 fixtures（`data/fixtures/hn_algolia.json`、`hf_daily_papers.json`）是 **独立合成信号**，不是 `papers.json` 副本。热源只进「热源雷达」，不进「主线动态」。

**缩写：** HN = Hacker News（黑客新闻）；HF = Hugging Face Papers（每日论文）。

产物：

| 路径 | 含义 |
| --- | --- |
| `runs/YYYY-MM-DD.json` | run status；每通道 `health`（`ok`/`unavailable`/`partial`）+ 样例 |
| `data/triage/YYYY-MM-DD.json` | 分诊队列（热度只提权） |
| `data/briefs/*.json` | 中文 Brief（含主线/短期标签） |
| `docs/digests/YYYY-MM-DD.md` | **读者主入口** 秘书周报 |

秘书周报固定区块（严格顺序，限时吸收）：

1. **今日/本周判断** — ≤3 句
2. **主线动态** — 仅 `horizon=mainline`（≤5）
3. **短期局部** — `horizon=near_term`（≤5，次要/可折叠阅读）
4. **热源雷达** — 按 score 优先的命中 + 通道覆盖健康（正常/降级）
5. **缺口与下周盯梢** — ≤5
6. **管道健康** — 紧凑表

## 在线全流程（需要网络）

```bash
python -m radar run
```

| 通道 | 角色 | 网络 | Token | 实际调用 |
| --- | --- | --- | --- | --- |
| arXiv Export API | discovery | 需要 | 无 | Atom 检索 |
| OpenReview API v2 | discovery | 需要 | 无（礼貌限速） | notes 搜索 |
| GitHub Search | discovery | 需要 | **建议** `GITHUB_TOKEN` | REST search |
| **Hacker News Algolia** | signal（热源） | 需要 | 无 | `hn.algolia.com` 查询 world model |
| **Hugging Face Daily Papers** | signal（热源） | 需要 | 通常无 | `huggingface.co/api/daily_papers` |

> 直播模式真实请求 HN 与 HF；失败记 `unavailable`/`partial`，**永不**写成「本周无新闻」。  
> MVP **不**接 X / YouTube 自动热源。

仅跑发现通道：

```bash
python -m radar run --discovery-only
```

## Brief 与校验

```bash
python -m radar seed-briefs
python -m radar validate-brief data/briefs/<paper-id>.json
```

发布硬门槛：`claim` / `map_position` / `do` / `evidence_links` / **`horizon`** / **`mainline_note`**  
（`fake_demand` 可空，有则在简报中显示）。

| 字段 | 含义 |
| --- | --- |
| `horizon=mainline` | **主线/长期**：改定义、评价、runtime 契约或多年度能力阶梯 |
| `horizon=near_term` | **短期/局部**：优化当下局部问题，不移动主线 |
| `mainline_note` | 一句中文：对长期主线的影响（或明确「不改主线」） |

`do` 必须以 **建 / 研 / 观望 / 忽略** 开头。读者向字段优先中文。

## 周审节奏（人工）

1. 读 `docs/digests/` 秘书周报：先判断 → 主线 →（可选）短期 → 热源。  
2. 在热源雷达与 `data/triage/` 挑高分候选，对照 [`inclusion-criteria.md`](./inclusion-criteria.md) 做一手源核验。  
3. 通过后写入 `data/papers.json`，标注将生成的 `horizon`，再 `seed-briefs` + 刷新周报。  
4. **讨论热度永不单独收录**；不可用 ≠ 零候选。

## 状态语义（必读）

- `success`：发现通道健康（允许个别 `empty`）  
- `partial`：部分通道失败或可选 signal 降级  
- `channel_down`：全部 **discovery** 不可用  
- `empty` = 健康但无命中；`unavailable` = 故障 —— **不可互换**
- 读者标签：`ok` / `unavailable` / `partial`

## 遗留脚本

`scripts/find_arxiv_candidates.py` 等仍可用；**默认路径**为 `python -m radar`。  
深读 HTML（`docs/reviews/`）为可选 Deep Read，不再作为默认交付。
