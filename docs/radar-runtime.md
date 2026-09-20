# Radar Runtime — 30 分钟跑通指南

目标：在干净环境里完成 **发现 → 分诊 → Brief → Weekly Digest**，并看懂 run status。

## 前置

- Python 3.10+（仅标准库；无需 pip 安装第三方包）
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

1. 从 `data/papers.json`（已核验清单 / ledger）生成 **核验 Brief**；
2. 用离线 fixtures 跑 **发现 + 热源** 适配器（arXiv / OpenReview / GitHub / Hacker News / Hugging Face Papers）；
3. 写出分诊队列、Weekly Digest、run status。

热源 fixtures（`data/fixtures/hn_algolia.json`、`hf_daily_papers.json`）是 **独立合成信号**，不是 `papers.json` 的副本——Digest 里「本周信号」与「核验 Brief」必须分开读。

产物：

| 路径 | 含义 |
| --- | --- |
| `runs/YYYY-MM-DD.json` | 机器可读 run status（`success` / `partial` / `channel_down`）；每通道含 `health`（`ok`/`unavailable`/`partial`）、`item_count`、样例标题/id/时间戳 |
| `data/triage/YYYY-MM-DD.json` | 分诊队列（证据 + confidence；热度只提权） |
| `data/briefs/*.json` | 中文 Brief（publish gate schema） |
| `docs/digests/YYYY-MM-DD.md` | **读者主入口** Weekly Digest |

Digest 固定区块：

1. **本周可带走的结论**（3–7 条决策）
2. **地图与缺口**（按 cluster）
3. **本周信号（热源/发现）** — 非清单副本
4. **核验 Brief（按 cluster）** — 来自已核验清单
5. **管道健康** — 每通道 `ok` / `unavailable` / `partial` + 条数 + 样例

## 在线全流程（需要网络）

```bash
python -m radar run
```

| 通道 | 角色 | 网络 | Token | 实际调用 |
| --- | --- | --- | --- | --- |
| arXiv Export API | discovery | 需要 | 无 | Atom 检索 |
| OpenReview API v2 | discovery | 需要 | 无（请礼貌限速） | notes 搜索 |
| GitHub Search | discovery | 需要 | **建议** `GITHUB_TOKEN` | REST search |
| **Hacker News Algolia** | signal（可选热源） | 需要 | 无 | `https://hn.algolia.com/api/v1/search?query=world+model&tags=story` |
| **Hugging Face Daily Papers** | signal（可选热源） | 需要 | 通常无；若限流可后续加 token | `https://huggingface.co/api/daily_papers` |

> 直播模式会 **真实请求** HN Algolia 与 HF Papers；失败记 `unavailable` / `partial`，**永不**叙述成「本周无新闻」。MVP **不**接 X / YouTube 自动热源。

仅跑发现通道：

```bash
python -m radar run --discovery-only
```

## Brief 与校验

从已核验 `data/papers.json` 重新生成 Brief：

```bash
python -m radar seed-briefs
python -m radar validate-brief data/briefs/<paper-id>.json
```

Brief 发布硬门槛字段：`claim` / `map_position` / `do` / `evidence_links`（`fake_demand` 可空，但 Digest 有则必显）。  
`do` 必须以 **建 / 研 / 观望 / 忽略** 之一开头。读者向字段优先中文。

## 周审节奏（人工）

1. 看 `docs/digests/` 本周 Digest 与 `runs/` status。  
2. 在「本周信号」与 `data/triage/` 里挑高 confidence 候选，对照 [`inclusion-criteria.md`](./inclusion-criteria.md) 做一手源核验。  
3. 通过后写入 `data/papers.json`，再 `seed-briefs` + 刷新 Digest。  
4. **讨论热度永不单独收录**；通道 `unavailable` 不得叙述成「本周无新闻」。

## 状态语义（必读）

- `success`：发现通道健康（允许个别通道 `empty`）  
- `partial`：部分通道失败或可选 signal 降级  
- `channel_down`：全部 **discovery** 通道不可用  
- 通道机器状态 `empty` = 健康但无命中；`unavailable` = 故障 —— **两者不可互换**
- Digest / manifest 读者标签：`ok`（success∪empty）/ `unavailable` / `partial`（error）

## 遗留脚本

`scripts/find_arxiv_candidates.py` 等仍可用作单通道工具；**默认路径**改为 `python -m radar`。深读 HTML（`docs/reviews/`）为可选 Deep Read，不再作为默认交付。
