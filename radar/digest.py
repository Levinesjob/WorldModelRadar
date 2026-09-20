"""秘书日报/周报（Secretary Briefing）生成器 — 主线优先、限时吸收。"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from radar.schemas import (
    SIGNAL_CHANNELS,
    ChannelResult,
    ChannelStatus,
    Horizon,
    HORIZON_ZH,
    RunStatus,
    channel_health_label,
    channel_samples,
    status_reader_copy,
)

# Fixed briefing blocks — strict reader order for limited daily time.
DIGEST_BLOCKS = (
    "judgment",  # 今日/本周判断 — ≤3 sentences
    "mainline",  # 主线动态 — ≤5
    "near_term",  # 短期局部 — ≤5
    "heat_radar",  # 热源雷达 — prioritized + coverage
    "gaps_and_watch",  # 缺口与下周盯梢 — ≤5
    "pipeline_health",  # 管道健康 — compact
)

CLUSTER_ORDER = ("runtime", "video_sim", "robot", "eval", "definition", "code")

ROLE_ZH = {
    "discovery": "发现",
    "signal": "热源/信号",
}

CHANNEL_ZH = {
    "arxiv": "arXiv（预印本库）",
    "openreview": "OpenReview（公开审稿平台）",
    "github": "GitHub（代码托管）",
    "hackernews": "Hacker News（HN，黑客新闻）",
    "huggingface": "Hugging Face Papers（HF Papers，每日论文）",
}

MAINLINE_LIMIT = 5
NEAR_TERM_LIMIT = 5
HEAT_LIMIT = 5
GAPS_WATCH_LIMIT = 5
JUDGMENT_SENTENCE_LIMIT = 3


def _action_prefix(do_value: str) -> str:
    text = (do_value or "").strip()
    for allowed in ("建", "研", "观望", "忽略"):
        if text.startswith(allowed):
            return allowed
    return "观望"


def _horizon_of(brief: dict[str, Any]) -> str:
    h = (brief.get("horizon") or "").strip()
    if h in (Horizon.MAINLINE.value, Horizon.NEAR_TERM.value):
        return h
    # Legacy briefs without field: treat core-ish map_position as mainline heuristic.
    pos = (brief.get("map_position") or "").lower()
    if " · core ·" in f" {pos} " or pos.startswith("definition") or "eval" in pos:
        if "adjacent" in pos or "domain" in pos:
            return Horizon.NEAR_TERM.value
        return Horizon.MAINLINE.value
    return Horizon.NEAR_TERM.value


def _brief_card(brief: dict[str, Any]) -> dict[str, Any]:
    horizon = _horizon_of(brief)
    return {
        "id": brief.get("id"),
        "title": brief.get("title") or brief.get("paper_id"),
        "claim": brief.get("claim"),
        "do": brief.get("do"),
        "action": _action_prefix(str(brief.get("do") or "")),
        "map_position": brief.get("map_position"),
        "fake_demand": brief.get("fake_demand") or "",
        "evidence_links": brief.get("evidence_links") or [],
        "cluster_id": brief.get("cluster_id") or "unknown",
        "horizon": horizon,
        "horizon_label": HORIZON_ZH.get(horizon, horizon),
        "mainline_note": (brief.get("mainline_note") or "").strip(),
        "source": "verified_ledger",
    }


def _action_rank(card: dict[str, Any]) -> int:
    return {"建": 0, "研": 1, "观望": 2, "忽略": 3}.get(card.get("action") or "", 9)


def _select_horizon_items(
    briefs: list[dict[str, Any]],
    horizon: str,
    *,
    limit: int,
) -> list[dict[str, Any]]:
    cards = [_brief_card(b) for b in briefs if _horizon_of(b) == horizon]
    cards.sort(key=lambda c: (_action_rank(c), (c.get("title") or "").lower()))
    # Drop 忽略 from primary lists unless we lack items.
    primary = [c for c in cards if c.get("action") != "忽略"]
    chosen = primary[:limit] if primary else cards[:limit]
    return chosen


def _build_judgment(
    *,
    run_status: RunStatus,
    mainline: list[dict[str, Any]],
    near_term: list[dict[str, Any]],
    heat_radar: dict[str, Any],
    channel_results: list[ChannelResult],
    judgment: str | None,
) -> list[str]:
    """1–3 sentences max — conclusions first for accurate absorption."""
    if judgment:
        # Split on Chinese/English sentence boundaries; clamp.
        parts = [p.strip() for p in judgment.replace("。", "。\n").split("\n") if p.strip()]
        sentences = []
        for part in parts:
            if part.endswith("。") or part.endswith(".") or part.endswith("！"):
                sentences.append(part)
            else:
                sentences.append(part if part.endswith("。") else part + "。")
            if len(sentences) >= JUDGMENT_SENTENCE_LIMIT:
                break
        return sentences[:JUDGMENT_SENTENCE_LIMIT]

    sentences: list[str] = []

    if run_status == RunStatus.CHANNEL_DOWN:
        sentences.append(
            "管道故障：全部发现通道不可用——这是运维问题，不是「领域无新闻」；本周勿据空结果下收录结论。"
        )
    elif run_status == RunStatus.PARTIAL:
        down = [
            r.channel
            for r in channel_results
            if r.status in (ChannelStatus.UNAVAILABLE, ChannelStatus.ERROR)
        ]
        sentences.append(
            f"管道部分降级（{', '.join(down) or '部分通道'}不可用）；已有通道结果可分诊，不可用 ≠ 零候选。"
        )

    if mainline:
        top = mainline[0]
        sentences.append(
            f"主线焦点：【{top.get('action')}】{(top.get('claim') or '').strip()}"
            f"（{top.get('mainline_note') or '触及长期能力阶梯'}）"
        )
    elif near_term:
        sentences.append(
            "本周核验面以短期/局部条目为主，尚无新的主线契约级变更；先观望场景切片，勿升格为领域转向。"
        )
    else:
        sentences.append("本周无新的核验 Brief 更新；以热源分诊与管道健康为准，勿把静默当成领域停摆。")

    hits = heat_radar.get("hits") or []
    if hits and len(sentences) < JUDGMENT_SENTENCE_LIMIT:
        top_hit = hits[0]
        why = top_hit.get("why_matters") or "热度只提权"
        sentences.append(
            f"热源优先关注「{top_hit.get('title')}」（{', '.join(top_hit.get('channels') or [])}）：{why}"
        )

    # Deduplicate / clamp
    seen: set[str] = set()
    out: list[str] = []
    for s in sentences:
        if s in seen:
            continue
        seen.add(s)
        out.append(s)
        if len(out) >= JUDGMENT_SENTENCE_LIMIT:
            break
    return out


def _build_map_and_gaps(
    briefs: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_cluster: dict[str, int] = {}
    for brief in briefs:
        cid = brief.get("cluster_id") or "unknown"
        by_cluster[cid] = by_cluster.get(cid, 0) + 1

    map_and_gaps: list[dict[str, Any]] = []
    known_ids = {c.get("id") for c in clusters}
    ordered = list(clusters)
    present = {c.get("id") for c in clusters}
    for cid in CLUSTER_ORDER:
        if cid not in present:
            ordered.append({"id": cid, "label": cid, "gap_note": ""})

    for cluster in ordered:
        cid = cluster.get("id")
        count = by_cluster.get(cid, 0)
        gap = cluster.get("gap_note") or ""
        map_and_gaps.append(
            {
                "cluster_id": cid,
                "label": cluster.get("label") or cid,
                "brief_count": count,
                "gap_note": gap,
                "note": gap if count == 0 else f"代表核验 Brief ×{count}",
                "has_gap": bool(gap) and count == 0,
            }
        )
    for cid, count in by_cluster.items():
        if cid not in known_ids and cid not in CLUSTER_ORDER:
            map_and_gaps.append(
                {
                    "cluster_id": cid,
                    "label": cid,
                    "brief_count": count,
                    "gap_note": "",
                    "note": f"未登记 cluster，Brief ×{count}",
                    "has_gap": False,
                }
            )
    return map_and_gaps


class _SignalMeta:
    __slots__ = ("discovered_at", "channel", "role", "metrics")

    def __init__(
        self,
        discovered_at: str,
        channel: str,
        role: str,
        metrics: dict[str, Any] | None = None,
    ) -> None:
        self.discovered_at = discovered_at
        self.channel = channel
        self.role = role
        self.metrics = metrics or {}


def _heat_score(cand: dict[str, Any], signal_meta: dict[str, _SignalMeta]) -> float:
    """Prioritize heat for limited daily time — never dump into mainline."""
    boost = float(cand.get("priority_boost") or 0.0)
    conf = {"high": 3.0, "medium": 1.5, "low": 0.5}.get(str(cand.get("confidence") or ""), 0.5)
    metric_bonus = 0.0
    for sid in cand.get("signal_ids") or []:
        meta = signal_meta.get(sid)
        if not meta:
            continue
        m = meta.metrics or {}
        # HN points / HF upvotes if present in fixture metrics
        for key in ("points", "num_comments", "upvotes", "reactions"):
            try:
                metric_bonus += float(m.get(key) or 0) * 0.01
            except (TypeError, ValueError):
                pass
    heat_channels = [ch for ch in (cand.get("channels") or []) if ch in SIGNAL_CHANNELS]
    channel_bonus = 2.0 if heat_channels else 0.5
    return boost * 10 + conf + metric_bonus + channel_bonus


def _why_heat_matters(cand: dict[str, Any]) -> str:
    channels = cand.get("channels") or []
    conf = cand.get("confidence") or "low"
    title = (cand.get("title") or "").lower()
    # Explicit noise: low confidence or off-topic HN chatter.
    wmish = any(
        k in title
        for k in ("world model", "worldmodel", "simulator", "embodied", "arxiv")
    )
    if conf == "low" and not wmish:
        return "噪声可忽略——低置信且未锚定世界模型主线。"
    if conf == "low" and not any(ch in SIGNAL_CHANNELS for ch in channels):
        return "噪声可忽略——低置信发现，未与热源交叉。"
    if "hackernews" in channels and "huggingface" in channels:
        return "HN+HF 双热源交叉，值得提权分诊（仍非核验门票）。"
    if "hackernews" in channels:
        return "HN 工程圈在讨论；核对是否触及 runtime/评价主线，否则作短期观察。"
    if "huggingface" in channels:
        return "HF Papers 圈内注意力；对齐 arXiv 后决定是否进入周审。"
    if "github" in channels:
        return "GitHub 采纳线索；看增速与 README 是否锚定论文，勿凭星标收录。"
    return "发现通道命中；热度只提权，需一手源核验。"

def _build_heat_radar(
    candidates: list[dict[str, Any]],
    channel_results: list[ChannelResult],
) -> dict[str, Any]:
    """Wide net, prioritized list — top heat hits + coverage health."""
    signal_meta: dict[str, _SignalMeta] = {}
    for result in channel_results:
        for signal in result.signals:
            signal_meta[signal.id] = _SignalMeta(
                discovered_at=signal.discovered_at,
                channel=signal.channel,
                role=result.role,
                metrics=signal.metrics if isinstance(signal.metrics, dict) else {},
            )

    items: list[dict[str, Any]] = []
    for cand in candidates:
        if cand.get("seeded_from_verified"):
            continue
        channels = list(cand.get("channels") or [])
        roles = sorted(
            {
                next((r.role for r in channel_results if r.channel == ch), "discovery")
                for ch in channels
            }
        )
        discovered_ats = []
        for sid in cand.get("signal_ids") or []:
            meta = signal_meta.get(sid)
            if meta and meta.discovered_at:
                discovered_ats.append(meta.discovered_at)
        score = _heat_score(cand, signal_meta)
        items.append(
            {
                "id": cand.get("id"),
                "title": cand.get("title"),
                "url": cand.get("url"),
                "channels": channels,
                "roles": roles,
                "confidence": cand.get("confidence"),
                "priority_boost": cand.get("priority_boost"),
                "score": round(score, 2),
                "signal_ids": cand.get("signal_ids") or [],
                "discovered_at": min(discovered_ats) if discovered_ats else None,
                "source": "heat_or_discovery",
                "why_matters": _why_heat_matters(cand),
                "note": "热源/发现信号——非核验清单；不进主线栏。",
            }
        )

    items.sort(key=lambda x: (-float(x.get("score") or 0), str(x.get("title") or "")))
    top = items[:HEAT_LIMIT]

    coverage: list[dict[str, Any]] = []
    for result in channel_results:
        coverage.append(
            {
                "channel": result.channel,
                "channel_label": CHANNEL_ZH.get(result.channel, result.channel),
                "role": result.role,
                "health": channel_health_label(result.status),
                "status": result.status.value,
                "item_count": result.item_count,
            }
        )

    return {
        "hits": top,
        "total_candidates": len(items),
        "coverage": coverage,
        "note": "广撒网后按分数优先；热度 ≠ 真理，永不单独收录。",
    }


def _build_gaps_and_watch(
    map_and_gaps: list[dict[str, Any]],
    heat_radar: dict[str, Any],
) -> list[dict[str, Any]]:
    """≤5 gap / next-week watch items."""
    items: list[dict[str, Any]] = []
    for gap in map_and_gaps:
        if gap.get("gap_note"):
            kind = "缺口" if gap.get("has_gap") else "持续关注"
            items.append(
                {
                    "kind": kind,
                    "cluster_id": gap.get("cluster_id"),
                    "label": gap.get("label"),
                    "text": gap.get("gap_note"),
                }
            )
        if len(items) >= GAPS_WATCH_LIMIT:
            break

    # If room, add top heat as watch (not mainline).
    if len(items) < GAPS_WATCH_LIMIT:
        for hit in heat_radar.get("hits") or []:
            items.append(
                {
                    "kind": "盯梢",
                    "cluster_id": None,
                    "label": "热源",
                    "text": f"跟进「{hit.get('title')}」——{hit.get('why_matters')}",
                }
            )
            if len(items) >= GAPS_WATCH_LIMIT:
                break
    return items[:GAPS_WATCH_LIMIT]


def _build_pipeline_health(channel_results: list[ChannelResult]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in channel_results:
        health = channel_health_label(result.status)
        samples = channel_samples(result, limit=2)
        latest = max((s["discovered_at"] for s in samples if s.get("discovered_at")), default=None)
        rows.append(
            {
                "channel": result.channel,
                "channel_label": CHANNEL_ZH.get(result.channel, result.channel),
                "role": result.role,
                "role_label": ROLE_ZH.get(result.role, result.role),
                "status": result.status.value,
                "health": health,
                "item_count": result.item_count,
                "error_code": result.error_code,
                "reader_copy": status_reader_copy(result.status),
                "message": result.message,
                "samples": samples,
                "latest_discovered_at": latest,
            }
        )
    return rows


def build_digest(
    *,
    run_status: RunStatus,
    channel_results: list[ChannelResult],
    briefs: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    clusters: list[dict[str, Any]] | None = None,
    judgment: str | None = None,
    week: str | None = None,
) -> dict[str, Any]:
    week = week or date.today().isoformat()
    clusters = clusters or []

    map_and_gaps = _build_map_and_gaps(briefs, clusters)
    mainline = _select_horizon_items(briefs, Horizon.MAINLINE.value, limit=MAINLINE_LIMIT)
    near_term = _select_horizon_items(briefs, Horizon.NEAR_TERM.value, limit=NEAR_TERM_LIMIT)
    heat_radar = _build_heat_radar(candidates, channel_results)
    gaps_and_watch = _build_gaps_and_watch(map_and_gaps, heat_radar)
    pipeline_health = _build_pipeline_health(channel_results)
    judgment_lines = _build_judgment(
        run_status=run_status,
        mainline=mainline,
        near_term=near_term,
        heat_radar=heat_radar,
        channel_results=channel_results,
        judgment=judgment,
    )

    # Legacy-compatible surfaces for older tooling.
    new_signals = heat_radar.get("hits") or []
    verified_flat = mainline + near_term

    return {
        "week": week,
        "run_status": run_status.value,
        "product": "secretary_briefing",
        "title_zh": "秘书周报",
        "labels": {
            "judgment": "今日/本周判断",
            "mainline": "主线动态（主线/长期）",
            "near_term": "短期局部（短期/局部优化）",
            "heat_radar": "热源雷达（广覆盖·强优先）",
            "gaps_and_watch": "缺口与下周盯梢",
            "pipeline_health": "管道健康",
            # legacy aliases
            "verified_briefs": "核验 Brief（已按主线/短期拆分）",
            "new_signals": "热源雷达命中（非清单副本）",
        },
        "blocks": {
            "judgment": judgment_lines,
            "mainline": mainline,
            "near_term": near_term,
            "heat_radar": heat_radar,
            "gaps_and_watch": gaps_and_watch,
            "pipeline_health": pipeline_health,
            # Backward-compatible aliases
            "takeaways": judgment_lines,
            "map_and_gaps": map_and_gaps,
            "new_signals": new_signals,
            "verified_briefs": [
                {
                    "cluster_id": "mainline",
                    "label": "主线/长期",
                    "brief_count": len(mainline),
                    "briefs": mainline,
                },
                {
                    "cluster_id": "near_term",
                    "label": "短期/局部",
                    "brief_count": len(near_term),
                    "briefs": near_term,
                },
            ],
            "one_line_judgment": judgment_lines[0] if judgment_lines else "",
            "map_changes": map_and_gaps,
            "new_briefs": verified_flat,
            "watchlist": gaps_and_watch,
        },
    }


def _render_brief_item(card: dict[str, Any], *, compact: bool = False) -> list[str]:
    lines: list[str] = []
    horizon_label = card.get("horizon_label") or HORIZON_ZH.get(card.get("horizon") or "", "")
    lines.append(f"- **【{horizon_label}·{card.get('action')}】** {card.get('claim')}")
    if card.get("mainline_note"):
        lines.append(f"  - 主线影响: {card.get('mainline_note')}")
    if not compact:
        title = card.get("title") or ""
        if title:
            lines.append(f"  - 标题: {title}")
        lines.append(f"  - 行动: {card.get('do')}")
        fake = (card.get("fake_demand") or "").strip()
        if fake:
            lines.append(f"  - 假需求: {fake}")
        links = ", ".join(card.get("evidence_links") or []) or "—"
        lines.append(f"  - 证据: {links}")
    else:
        lines.append(f"  - 行动: {card.get('do')}")
    return lines


def render_digest_markdown(digest: dict[str, Any]) -> str:
    blocks = digest["blocks"]
    title_zh = digest.get("title_zh") or "秘书周报"
    lines = [
        f"# WorldModel Radar · {title_zh} — {digest['week']}",
        "",
        f"_run_status: `{digest['run_status']}` · 秘书简报（非信息倾销）_",
        "",
        "## 1. 今日/本周判断",
        "",
    ]
    judgment = blocks.get("judgment") or blocks.get("takeaways") or []
    if judgment:
        for item in judgment:
            text = item if str(item).endswith(("。", "！", "？", ".", "!", "?")) else f"{item}"
            lines.append(f"- {text}")
    else:
        lines.append("- （暂无判断）")

    lines += ["", "## 2. 主线动态", "", "_仅主线/长期条目（≤5）；改定义·评价·runtime 契约或多年度能力阶梯_", ""]
    mainline = blocks.get("mainline") or []
    if mainline:
        for card in mainline:
            lines.extend(_render_brief_item(card, compact=False))
    else:
        lines.append("- （本周无主线级核验更新）")

    lines += ["", "## 3. 短期局部", "", "_短期/局部优化（≤5）；次要阅读，勿升格为主线_", ""]
    near_term = blocks.get("near_term") or []
    if near_term:
        for card in near_term:
            lines.extend(_render_brief_item(card, compact=True))
    else:
        lines.append("- （本周无短期/局部条目）")

    heat = blocks.get("heat_radar") or {}
    lines += [
        "",
        "## 4. 热源雷达",
        "",
        f"_{digest.get('labels', {}).get('heat_radar', '热源雷达')}：{heat.get('note', '')}_",
        "",
        "### 优先命中",
        "",
    ]
    hits = heat.get("hits") or blocks.get("new_signals") or []
    if hits:
        for sig in hits:
            chans = ", ".join(sig.get("channels") or []) or "—"
            url = sig.get("url") or "#"
            score = sig.get("score")
            score_bit = f" · score={score}" if score is not None else ""
            lines.append(f"- [{sig.get('title')}]({url})")
            lines.append(
                f"  - 通道: `{chans}` · confidence={sig.get('confidence')}{score_bit}"
            )
            if sig.get("signal_ids"):
                lines.append(f"  - 信号 id: {', '.join(sig['signal_ids'])}")
            lines.append(f"  - 为何看: {sig.get('why_matters') or sig.get('note')}")
    else:
        lines.append("- （本周无优先热源命中；若覆盖为 unavailable，勿解读为领域静默）")

    lines += ["", "### 覆盖健康", ""]
    coverage = heat.get("coverage") or []
    if coverage:
        ok = [c for c in coverage if c.get("health") == "ok"]
        down = [c for c in coverage if c.get("health") != "ok"]
        ok_names = ", ".join(c.get("channel_label") or c.get("channel") for c in ok) or "无"
        down_names = ", ".join(
            f"{c.get('channel_label') or c.get('channel')}(`{c.get('health')}`)" for c in down
        ) or "无"
        lines.append(f"- 正常: {ok_names}")
        lines.append(f"- 异常/降级: {down_names}")
        lines.append(f"- 分诊候选总数: {heat.get('total_candidates', len(hits))}（上表仅优先 ≤{HEAT_LIMIT}）")
    else:
        lines.append("- （无覆盖数据）")

    lines += ["", "## 5. 缺口与下周盯梢", ""]
    gaps = blocks.get("gaps_and_watch") or []
    if gaps:
        for item in gaps:
            kind = item.get("kind") or "盯梢"
            label = item.get("label") or item.get("cluster_id") or ""
            lines.append(f"- 【{kind}·{label}】{item.get('text')}")
    else:
        lines.append("- （暂无缺口/盯梢）")

    lines += ["", "## 6. 管道健康", ""]
    lines.append("| 通道 | 角色 | 健康 | 条数 | 说明 |")
    lines.append("| --- | --- | --- | ---: | --- |")
    for row in blocks.get("pipeline_health") or []:
        label = row.get("channel_label") or row.get("channel")
        role = row.get("role_label") or row.get("role")
        lines.append(
            f"| {label} | {role} | `{row.get('health')}` | "
            f"{row.get('item_count')} | {row.get('reader_copy')} |"
        )
    lines.append("")
    lines.append(
        "> 健康：`ok` / `unavailable` / `partial`。"
        "不可用 ≠ 零候选。热源（HN / HF Papers）只提权，不进主线栏。"
        "每条核验 Brief 必标 **主线/长期** 或 **短期/局部**。"
    )
    lines.append("")
    return "\n".join(lines)


def write_digest(out_dir: Path, digest: dict[str, Any]) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    week = digest["week"]
    json_path = out_dir / f"{week}.json"
    md_path = out_dir / f"{week}.md"
    json_path.write_text(json.dumps(digest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_digest_markdown(digest), encoding="utf-8")
    return json_path, md_path
