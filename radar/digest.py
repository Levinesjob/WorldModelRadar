"""Weekly Digest generator — structured Chinese extraction for decisions."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from radar.schemas import (
    SIGNAL_CHANNELS,
    ChannelResult,
    ChannelStatus,
    RunStatus,
    channel_health_label,
    channel_samples,
    status_reader_copy,
)

# Fixed Digest blocks (reader navigation order).
DIGEST_BLOCKS = (
    "takeaways",
    "map_and_gaps",
    "new_signals",
    "verified_briefs",
    "pipeline_health",
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


def _action_prefix(do_value: str) -> str:
    text = (do_value or "").strip()
    for allowed in ("建", "研", "观望", "忽略"):
        if text.startswith(allowed):
            return allowed
    return "观望"


def _brief_card(brief: dict[str, Any]) -> dict[str, Any]:
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
        "source": "verified_ledger",
    }


def _build_takeaways(
    *,
    run_status: RunStatus,
    briefs: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    map_and_gaps: list[dict[str, Any]],
    channel_results: list[ChannelResult],
) -> list[str]:
    """3–7 decision bullets — not a paper dump."""
    takeaways: list[str] = []

    if run_status == RunStatus.CHANNEL_DOWN:
        takeaways.append(
            "管道故障：全部发现通道不可用——这是运维问题，不是「领域无新闻」；本周勿据空结果下收录结论。"
        )
    elif run_status == RunStatus.PARTIAL:
        down = [
            r.channel
            for r in channel_results
            if r.status in (ChannelStatus.UNAVAILABLE, ChannelStatus.ERROR)
        ]
        takeaways.append(
            f"管道部分降级（{', '.join(down) or '部分通道'}不可用）；已有通道结果可分诊，不可用 ≠ 零候选。"
        )

    # Prioritize actionable verified briefs (建/研 first, then 观望).
    ranked = sorted(
        briefs,
        key=lambda b: {"建": 0, "研": 1, "观望": 2, "忽略": 3}.get(_action_prefix(str(b.get("do") or "")), 9),
    )
    for brief in ranked:
        action = _action_prefix(str(brief.get("do") or ""))
        if action == "忽略":
            continue
        claim = (brief.get("claim") or "").strip()
        if not claim:
            continue
        cluster = brief.get("cluster_id") or "?"
        takeaways.append(f"【{action}·{cluster}】{claim}")
        if len(takeaways) >= 5:
            break

    # Surface gaps that still have zero briefs.
    for gap in map_and_gaps:
        if gap.get("brief_count", 0) == 0 and gap.get("gap_note"):
            takeaways.append(f"【缺口·{gap.get('cluster_id')}】{gap['gap_note']}")
            if len(takeaways) >= 6:
                break

    # Heat/discovery signals this run (explicitly not ledger).
    heat = [
        c
        for c in candidates
        if not c.get("seeded_from_verified")
        and any(ch in SIGNAL_CHANNELS for ch in (c.get("channels") or []))
    ]
    if heat:
        top = heat[0]
        chans = ", ".join(top.get("channels") or [])
        takeaways.append(
            f"【信号·热源】本周热源命中「{top.get('title')}」（通道：{chans}）——只提权分诊，不自动进核验清单。"
        )

    # Deduplicate while preserving order; clamp 3–7.
    seen: set[str] = set()
    unique: list[str] = []
    for line in takeaways:
        if line in seen:
            continue
        seen.add(line)
        unique.append(line)
    if len(unique) < 3 and briefs:
        for brief in ranked:
            line = f"【{_action_prefix(str(brief.get('do') or ''))}】{(brief.get('claim') or '').strip()}"
            if line not in seen and (brief.get("claim") or "").strip():
                unique.append(line)
                seen.add(line)
            if len(unique) >= 3:
                break
    return unique[:7]


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
    # Stable fallback order for known cluster ids missing from file.
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
    __slots__ = ("discovered_at", "channel", "role")

    def __init__(self, discovered_at: str, channel: str, role: str) -> None:
        self.discovered_at = discovered_at
        self.channel = channel
        self.role = role


def _build_new_signals(
    candidates: list[dict[str, Any]],
    channel_results: list[ChannelResult],
) -> list[dict[str, Any]]:
    """Channel-attributed discovery + heat hits from this run (not ledger)."""
    signal_meta: dict[str, _SignalMeta] = {}
    for result in channel_results:
        for signal in result.signals:
            signal_meta[signal.id] = _SignalMeta(
                discovered_at=signal.discovered_at,
                channel=signal.channel,
                role=result.role,
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
        # Prefer earliest discovered_at among linked signals.
        discovered_ats = []
        for sid in cand.get("signal_ids") or []:
            meta = signal_meta.get(sid)
            if meta and meta.discovered_at:
                discovered_ats.append(meta.discovered_at)
        items.append(
            {
                "id": cand.get("id"),
                "title": cand.get("title"),
                "url": cand.get("url"),
                "channels": channels,
                "roles": roles,
                "confidence": cand.get("confidence"),
                "priority_boost": cand.get("priority_boost"),
                "signal_ids": cand.get("signal_ids") or [],
                "discovered_at": min(discovered_ats) if discovered_ats else None,
                "source": "heat_or_discovery",
                "note": "本周热源/发现信号——非核验清单条目；热度只提权。",
            }
        )
    return items


def _build_verified_by_cluster(
    briefs: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    label_by_id = {c.get("id"): c.get("label") or c.get("id") for c in clusters}
    buckets: dict[str, list[dict[str, Any]]] = {cid: [] for cid in CLUSTER_ORDER}
    extras: dict[str, list[dict[str, Any]]] = {}

    for brief in briefs:
        card = _brief_card(brief)
        cid = card["cluster_id"]
        if cid in buckets:
            buckets[cid].append(card)
        else:
            extras.setdefault(cid, []).append(card)

    # Within cluster: 建/研/观望/忽略, then title.
    action_rank = {"建": 0, "研": 1, "观望": 2, "忽略": 3}

    def sort_key(card: dict[str, Any]) -> tuple:
        return (action_rank.get(card.get("action") or "", 9), (card.get("title") or "").lower())

    groups: list[dict[str, Any]] = []
    for cid in CLUSTER_ORDER:
        cards = sorted(buckets.get(cid, []), key=sort_key)
        groups.append(
            {
                "cluster_id": cid,
                "label": label_by_id.get(cid, cid),
                "brief_count": len(cards),
                "briefs": cards,
            }
        )
    for cid, cards in extras.items():
        groups.append(
            {
                "cluster_id": cid,
                "label": label_by_id.get(cid, cid),
                "brief_count": len(cards),
                "briefs": sorted(cards, key=sort_key),
            }
        )
    return groups


def _build_pipeline_health(channel_results: list[ChannelResult]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in channel_results:
        health = channel_health_label(result.status)
        samples = channel_samples(result, limit=3)
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
    new_signals = _build_new_signals(candidates, channel_results)
    verified_briefs = _build_verified_by_cluster(briefs, clusters)
    pipeline_health = _build_pipeline_health(channel_results)

    if judgment:
        takeaways = [judgment]
        # Still fill to at least a few decision bullets when possible.
        extra = _build_takeaways(
            run_status=run_status,
            briefs=briefs,
            candidates=candidates,
            map_and_gaps=map_and_gaps,
            channel_results=channel_results,
        )
        for line in extra:
            if line not in takeaways and len(takeaways) < 7:
                takeaways.append(line)
    else:
        takeaways = _build_takeaways(
            run_status=run_status,
            briefs=briefs,
            candidates=candidates,
            map_and_gaps=map_and_gaps,
            channel_results=channel_results,
        )

    return {
        "week": week,
        "run_status": run_status.value,
        "labels": {
            "verified_briefs": "核验 Brief（来自已核验清单 / ledger）",
            "new_signals": "本周信号（来自热源/发现通道，非清单副本）",
        },
        "blocks": {
            "takeaways": takeaways,
            "map_and_gaps": map_and_gaps,
            "new_signals": new_signals,
            "verified_briefs": verified_briefs,
            "pipeline_health": pipeline_health,
            # Backward-compatible aliases used by older tests / tooling.
            "one_line_judgment": takeaways[0] if takeaways else "",
            "map_changes": map_and_gaps,
            "new_briefs": [card for g in verified_briefs for card in g["briefs"]],
            "watchlist": new_signals[:5],
        },
    }


def render_digest_markdown(digest: dict[str, Any]) -> str:
    blocks = digest["blocks"]
    lines = [
        f"# WorldModel Radar Weekly Digest — {digest['week']}",
        "",
        f"_run_status: `{digest['run_status']}`_",
        "",
        "## 本周可带走的结论",
        "",
    ]
    takeaways = blocks.get("takeaways") or []
    if takeaways:
        for item in takeaways:
            lines.append(f"- {item}")
    else:
        lines.append("- （暂无结论）")

    lines += ["", "## 地图与缺口", ""]
    for item in blocks.get("map_and_gaps") or []:
        extra = ""
        # When coverage > 0, still surface the standing gap as a secondary note.
        if not item.get("has_gap") and item.get("gap_note"):
            extra = f" · 持续关注：{item['gap_note']}"
        lines.append(
            f"- **{item['label']}** (`{item['cluster_id']}`): {item['note']}{extra}"
        )
    if not blocks.get("map_and_gaps"):
        lines.append("- （暂无 cluster 数据）")

    lines += [
        "",
        "## 本周信号（热源/发现）",
        "",
        f"_{digest.get('labels', {}).get('new_signals', '本周信号（热源/发现）')}_",
        "",
    ]
    signals = blocks.get("new_signals") or []
    if signals:
        for sig in signals:
            chans = ", ".join(sig.get("channels") or []) or "—"
            roles = ", ".join(sig.get("roles") or []) or "—"
            ts = sig.get("discovered_at") or "—"
            url = sig.get("url") or "#"
            lines.append(f"- [{sig.get('title')}]({url})")
            lines.append(
                f"  - 通道: `{chans}` · 角色: {roles} · confidence={sig.get('confidence')} · 时间: `{ts}`"
            )
            if sig.get("signal_ids"):
                lines.append(f"  - 信号 id: {', '.join(sig['signal_ids'])}")
            lines.append(f"  - 说明: {sig.get('note')}")
    else:
        lines.append("- （本周无新的热源/发现信号；若管道健康为 unavailable，勿解读为领域静默）")

    lines += [
        "",
        "## 核验 Brief（按 cluster）",
        "",
        f"_{digest.get('labels', {}).get('verified_briefs', '核验 Brief（来自已核验清单）')}_",
        "",
    ]
    groups = blocks.get("verified_briefs") or []
    any_brief = False
    for group in groups:
        cards = group.get("briefs") or []
        if not cards:
            continue
        any_brief = True
        lines.append(f"### {group.get('label')} (`{group.get('cluster_id')}`)")
        lines.append("")
        for card in cards:
            links = ", ".join(card.get("evidence_links") or []) or "—"
            lines.append(f"- **结论/行动**: {card.get('do')}")
            lines.append(f"  - 主张: {card.get('claim')}")
            title = card.get("title") or ""
            lines.append(f"  - 标题: {title}")
            lines.append(f"  - 位置: {card.get('map_position')}")
            fake = (card.get("fake_demand") or "").strip()
            if fake:
                lines.append(f"  - 易误读/假需求: {fake}")
            lines.append(f"  - 证据: {links}")
        lines.append("")
    if not any_brief:
        lines.append("- （本周无核验 Brief）")
        lines.append("")

    lines += ["## 管道健康", ""]
    lines.append("| 通道 | 角色 | 健康 | 机器状态 | 条数 | 样例（标题 / id / 时间） | 说明 |")
    lines.append("| --- | --- | --- | --- | ---: | --- | --- |")
    for row in blocks.get("pipeline_health") or []:
        samples = row.get("samples") or []
        if samples:
            sample_bits = []
            for s in samples:
                title = (s.get("title") or "")[:40]
                sample_bits.append(f"{title} (`{s.get('id')}`, {s.get('discovered_at') or '—'})")
            sample_txt = "<br>".join(sample_bits)
        else:
            sample_txt = "—"
        label = row.get("channel_label") or row.get("channel")
        role = row.get("role_label") or row.get("role")
        lines.append(
            f"| {label} | {role} | `{row.get('health')}` | `{row.get('status')}` | "
            f"{row.get('item_count')} | {sample_txt} | {row.get('reader_copy')} |"
        )
    lines.append("")
    lines.append(
        "> 健康取值：`ok` / `unavailable` / `partial`。"
        "不可用 ≠ 零候选；勿把通道故障叙述成「本周无新闻」。"
        "热源（HN / HF Papers）与核验清单必须分开阅读。"
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
