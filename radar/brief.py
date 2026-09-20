"""Brief generation and schema validation helpers."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from radar.schemas import Brief, validate_brief

# Map paper area keywords → cluster ids (see data/clusters.json).
AREA_CLUSTER_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"robot|embodied|action model|physical intelligence|vla", re.I), "robot"),
    (re.compile(r"driv|counterfactual|autonom", re.I), "robot"),
    (re.compile(r"video|generative foundation|interactive video", re.I), "video_sim"),
    (re.compile(r"simulat|admissib|physical grounding|actionable", re.I), "runtime"),
    (re.compile(r"evaluat|benchmark|decision-making-centric", re.I), "eval"),
    (re.compile(r"definition|roadmap|taxonomy|framing|openworldlib|graph world", re.I), "definition"),
    (re.compile(r"code|openworldlib|unified codebase", re.I), "code"),
    (re.compile(r"medical|economic|edge|digital twin", re.I), "runtime"),
]

# Reader-facing Chinese claims (≤150 chars). Keys = papers.json id.
CLAIM_ZH_BY_ID: dict[str, str] = {
    "chen-2026-definition-roadmap-world-models": "给出世界模型的科学定义、关键技术面与分阶段路线图，作领域总览入口。",
    "chen-2026-generative-engines-actionable-simulators": "主张从「好看的生成引擎」转向「可行动的物理 grounding 模拟器」。",
    "han-2026-economic-world-models": "把经济世界模型定义为可执行生成环境，并给出六级能力阶梯与工程蓝图。",
    "hou-2026-world-model-robot-learning": "从机器人学习视角系统综述世界模型：策略、学习型模拟器与视频世界模型。",
    "hu-2026-evolution-video-generative-foundations": "泛视频生成综述；仅在把高级视频生成通向世界模型时作边界对照。",
    "karcini-2026-robots-need-more-than-vla-world-models": "立场文：机器人不能只靠 VLA（Vision-Language-Action，视觉-语言-动作）与世界模型。",
    "liang-2026-world-action-models-embodied-brains": "梳理世界动作模型演进，诊断表征/标准/系统缺口，提出具身栈契约。",
    "liu-2026-graph-world-models": "形式化图世界模型范式，并用关系归纳偏置 taxonomy（分类体系）组织现有工作。",
    "liu-2026-interactive-video-world-modeling": "系统综述交互式视频世界建模的前沿、挑战、基准与趋势。",
    "liu-2026-medical-world-models": "整理医疗世界模型散点工作，围绕患者状态、临床动力学与干预策略建路线图。",
    "maharaj-2026-code-world-modelling-survey": "在代码智能非自回归范式综述中，把 Code World Models 作为一类关键路径。",
    "mei-2026-video-generation-models-robotics": "综述视频模型在机器人中作为具身世界模型的应用、挑战与方向。",
    "oefinger-2026-admissibility-world-model-simulators": "定义 L0–L4 可采信框架：何时可把世界模型模拟器判决当作保证证据。",
    "wang-2026-world-action-models": "定义世界动作模型为「世界模型+具身行动」范式，并综述架构/数据/评价。",
    "yu-2026-decision-centric-world-model-evaluation": "主张以决策为中心评价世界模型，提出 L0–L7 证据阶梯并诊断主张/证据错配。",
    "zeng-2026-openworldlib": "提出高级世界模型统一定义与能力分类，并给出标准化推理代码基座。",
    "zeng-2026-world-models-not-merely-injecting-world-knowledge": "批评「往任务里灌世界知识」的碎片化做法，主张更统一的通用世界模型规格。",
    "zhang-2026-driving-world-model-counterfactual-prediction": "指出驾驶世界模型在反事实预测上的协议缺口，并给出可控评测基准。",
    "zheng-2026-digital-twins-world-models-edge": "综述数字孪生走向世界模型，及其在移动边缘通用智能中的机会与挑战。",
}


def infer_cluster(area: str, title: str = "") -> str:
    text = f"{area} {title}"
    for pattern, cluster_id in AREA_CLUSTER_RULES:
        if pattern.search(text):
            return cluster_id
    return "definition"


def do_from_relevance(relevance: str) -> str:
    if relevance == "core":
        return "研 — 领域级 framing，值得跟定义与评价争论"
    if relevance == "domain":
        return "观望 — 领域切片，跟场景成熟度与可迁移协议"
    return "忽略 — adjacent；仅作边界对照，不进主清单决策"


def claim_zh_from_paper(paper: dict[str, Any]) -> str:
    """Prefer curated Chinese claim; fall back to compressed why_included / title."""
    paper_id = paper.get("id") or ""
    if paper_id in CLAIM_ZH_BY_ID:
        return CLAIM_ZH_BY_ID[paper_id]
    why = (paper.get("why_included") or "").strip()
    title = (paper.get("title") or "").strip()
    src = why or title
    return src if len(src) <= 150 else src[:147] + "…"


def brief_from_paper(paper: dict[str, Any]) -> Brief:
    """Derive a scannable Chinese brief from a verified paper record."""
    paper_id = paper.get("id") or ""
    title = paper.get("title") or ""
    area = paper.get("area") or ""
    relevance = paper.get("relevance") or "adjacent"
    cluster = infer_cluster(area, title)
    claim = claim_zh_from_paper(paper)

    evidence = []
    if paper.get("url"):
        evidence.append(paper["url"])
    if paper.get("repository"):
        evidence.append(paper["repository"])
    if not evidence and paper.get("arxiv_id"):
        evidence.append(f"https://arxiv.org/abs/{paper['arxiv_id']}")

    return Brief(
        id=f"brief-{paper_id}",
        paper_id=paper_id,
        title=title,
        claim=claim,
        map_position=f"{cluster} · {relevance} · {area}",
        do=do_from_relevance(relevance),
        fake_demand="把讨论热度或星标当成收录理由（热度只提权，不单独进核验清单）",
        evidence_links=evidence,
        cluster_id=cluster,
    )


def write_brief(path: Path, brief: Brief) -> list[str]:
    """Validate and write brief JSON. Returns validation errors (empty if ok)."""
    payload = brief.to_dict()
    errors = validate_brief(payload)
    if errors:
        return errors
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return []


def load_briefs(briefs_dir: Path) -> list[dict[str, Any]]:
    if not briefs_dir.exists():
        return []
    briefs = []
    for path in sorted(briefs_dir.glob("*.json")):
        briefs.append(json.loads(path.read_text(encoding="utf-8")))
    return briefs


def seed_briefs_from_papers(papers: list[dict[str, Any]], briefs_dir: Path) -> tuple[int, list[str]]:
    """Generate brief files for all papers; return (written, error messages)."""
    written = 0
    errors: list[str] = []
    briefs_dir.mkdir(parents=True, exist_ok=True)
    for paper in papers:
        brief = brief_from_paper(paper)
        path = briefs_dir / f"{brief.paper_id}.json"
        errs = write_brief(path, brief)
        if errs:
            errors.append(f"{brief.paper_id}: {', '.join(errs)}")
        else:
            written += 1
    return written, errors
