"""Weekly Digest generator — primary reader entry (five fixed blocks)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from radar.schemas import ChannelResult, ChannelStatus, RunStatus, status_reader_copy


DIGEST_BLOCKS = (
    "one_line_judgment",
    "map_changes",
    "new_briefs",
    "pipeline_health",
    "watchlist",
)


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

    # 1) One-line judgment
    if judgment:
        one_line = judgment
    elif run_status == RunStatus.CHANNEL_DOWN:
        one_line = (
            "本周发现通道全部不可用——这是管道故障，不是「领域无新闻」；"
            "请勿据空结果下结论。"
        )
    elif run_status == RunStatus.PARTIAL:
        down = [r.channel for r in channel_results if r.status in (ChannelStatus.UNAVAILABLE, ChannelStatus.ERROR)]
        one_line = (
            f"本周管道部分降级（{', '.join(down) or '部分通道'}不可用）；"
            "已有通道结果可分诊，不可用通道≠零候选。"
        )
    else:
        n_new = sum(1 for c in candidates if not c.get("seeded_from_verified"))
        one_line = (
            f"本周发现正常：分诊队列 {len(candidates)} 条"
            f"（含新信号约 {n_new}）；以 Brief 与地图变化为准，热度只提权。"
        )

    # 2) Map changes — cluster coverage from briefs
    by_cluster: dict[str, int] = {}
    for b in briefs:
        cid = b.get("cluster_id") or "unknown"
        by_cluster[cid] = by_cluster.get(cid, 0) + 1
    map_changes = []
    known_ids = {c.get("id") for c in clusters}
    for cluster in clusters:
        cid = cluster.get("id")
        count = by_cluster.get(cid, 0)
        gap = cluster.get("gap_note") or ""
        map_changes.append(
            {
                "cluster_id": cid,
                "label": cluster.get("label") or cid,
                "brief_count": count,
                "note": gap if count == 0 else f"代表 Brief ×{count}",
            }
        )
    for cid, count in by_cluster.items():
        if cid not in known_ids:
            map_changes.append(
                {
                    "cluster_id": cid,
                    "label": cid,
                    "brief_count": count,
                    "note": f"未登记 cluster，Brief ×{count}",
                }
            )

    # 3) New briefs (scannable)
    new_briefs = [
        {
            "id": b.get("id"),
            "title": b.get("title") or b.get("paper_id"),
            "claim": b.get("claim"),
            "map_position": b.get("map_position"),
            "do": b.get("do"),
            "evidence_links": b.get("evidence_links") or [],
        }
        for b in briefs
    ]

    # 4) Pipeline health — explicit unavailable ≠ empty
    pipeline_health = []
    for result in channel_results:
        pipeline_health.append(
            {
                "channel": result.channel,
                "role": result.role,
                "status": result.status.value,
                "item_count": result.item_count,
                "error_code": result.error_code,
                "reader_copy": status_reader_copy(result.status),
                "message": result.message,
            }
        )

    # 5) Watchlist ≤5 — prefer heat-boosted / github artifacts
    watchlist = []
    for cand in candidates:
        if cand.get("seeded_from_verified"):
            continue
        if len(watchlist) >= 5:
            break
        watchlist.append(
            {
                "title": cand.get("title"),
                "url": cand.get("url"),
                "channels": cand.get("channels"),
                "confidence": cand.get("confidence"),
                "priority_boost": cand.get("priority_boost"),
            }
        )

    return {
        "week": week,
        "run_status": run_status.value,
        "blocks": {
            "one_line_judgment": one_line,
            "map_changes": map_changes,
            "new_briefs": new_briefs,
            "pipeline_health": pipeline_health,
            "watchlist": watchlist,
        },
    }


def render_digest_markdown(digest: dict[str, Any]) -> str:
    blocks = digest["blocks"]
    lines = [
        f"# WorldModel Radar Weekly Digest — {digest['week']}",
        "",
        f"_run_status: `{digest['run_status']}`_",
        "",
        "## 1. 本周一句话判断",
        "",
        blocks["one_line_judgment"],
        "",
        "## 2. 地图变化",
        "",
    ]
    for item in blocks["map_changes"]:
        lines.append(f"- **{item['label']}** (`{item['cluster_id']}`): {item['note']}")
    if not blocks["map_changes"]:
        lines.append("- （暂无 cluster 数据）")

    lines += ["", "## 3. 新 Brief", ""]
    for b in blocks["new_briefs"]:
        links = ", ".join(b.get("evidence_links") or []) or "—"
        lines.append(f"- **{b.get('title')}**")
        lines.append(f"  - 主张: {b.get('claim')}")
        lines.append(f"  - 位置: {b.get('map_position')}")
        lines.append(f"  - 建议: {b.get('do')}")
        lines.append(f"  - 证据: {links}")
    if not blocks["new_briefs"]:
        lines.append("- （本周无新 Brief）")

    lines += ["", "## 4. 管道健康", ""]
    lines.append("| Channel | Role | Status | Count | Note |")
    lines.append("| --- | --- | --- | ---: | --- |")
    for row in blocks["pipeline_health"]:
        lines.append(
            f"| {row['channel']} | {row['role']} | `{row['status']}` | {row['item_count']} | {row['reader_copy']} |"
        )
    lines.append("")
    lines.append("> 不可用 ≠ 零候选；勿把通道故障叙述成「本周无新闻」。")

    lines += ["", "## 5. 下周盯什么（≤5）", ""]
    for w in blocks["watchlist"]:
        lines.append(f"- [{w.get('title')}]({w.get('url')}) — channels={w.get('channels')} confidence={w.get('confidence')}")
    if not blocks["watchlist"]:
        lines.append("- （空：可能是管道降级或本周无未核验新信号）")
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
