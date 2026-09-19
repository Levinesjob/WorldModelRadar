"""Radar Runtime schemas and status vocabulary.

Status rules (MVP):
- Channel outage / timeout / auth failure → ``unavailable`` (never narrate as empty).
- Successful fetch with zero hits → ``empty``.
- Successful fetch with hits → ``success``.
- Aggregate run: all discovery ok → ``success``; some fail → ``partial``;
  all discovery down → ``channel_down``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ChannelStatus(str, Enum):
    SUCCESS = "success"
    EMPTY = "empty"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


class RunStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    CHANNEL_DOWN = "channel_down"
    ERROR = "error"


# Discovery adapters must succeed (or empty) for a clean run.
DISCOVERY_CHANNELS = ("arxiv", "openreview", "github")
# Optional signal adapters: degradable; failure is never "zero candidates".
SIGNAL_CHANNELS = ("hackernews", "huggingface")


BRIEF_REQUIRED_FIELDS = ("claim", "map_position", "do", "evidence_links")
BRIEF_OPTIONAL_FIELDS = ("fake_demand",)
DO_ALLOWED = ("建", "研", "观望", "忽略")


@dataclass
class Signal:
    """Raw discovery from any channel."""

    id: str
    channel: str
    title: str
    url: str
    discovered_at: str
    summary: str = ""
    evidence: list[str] = field(default_factory=list)
    confidence: str = "low"  # high | medium | low
    anchors: dict[str, str] = field(default_factory=dict)  # arxiv_id, repo, etc.
    metrics: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Candidate:
    """Triage-queue item with evidence + confidence."""

    id: str
    title: str
    url: str
    channels: list[str]
    confidence: str
    evidence: list[str]
    signal_ids: list[str]
    anchors: dict[str, str] = field(default_factory=dict)
    summary: str = ""
    priority_boost: float = 0.0
    requires_manual_inclusion_review: bool = True
    seeded_from_verified: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Brief:
    """Chinese publish-gate brief (schema-first)."""

    id: str
    paper_id: str
    claim: str
    map_position: str
    do: str
    evidence_links: list[str]
    fake_demand: str = ""
    title: str = ""
    cluster_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ChannelResult:
    channel: str
    role: str  # discovery | signal
    status: ChannelStatus
    item_count: int = 0
    signals: list[Signal] = field(default_factory=list)
    error_code: str | None = None
    message: str = ""
    duration_ms: int = 0
    endpoint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "channel": self.channel,
            "role": self.role,
            "status": self.status.value,
            "item_count": self.item_count,
            "error_code": self.error_code,
            "message": self.message,
            "duration_ms": self.duration_ms,
            "endpoint": self.endpoint,
            "signals": [s.to_dict() for s in self.signals],
        }


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def aggregate_run_status(channel_results: list[ChannelResult]) -> RunStatus:
    """Compute machine-readable run status from per-channel results.

    Discovery channels drive overall health. Signal failures never force
    ``channel_down`` alone; they contribute to ``partial`` when discovery is ok.
    """
    discovery = [r for r in channel_results if r.role == "discovery"]
    signals = [r for r in channel_results if r.role == "signal"]

    if not discovery:
        return RunStatus.ERROR

    def is_up(r: ChannelResult) -> bool:
        return r.status in (ChannelStatus.SUCCESS, ChannelStatus.EMPTY)

    def is_down(r: ChannelResult) -> bool:
        return r.status in (ChannelStatus.UNAVAILABLE, ChannelStatus.ERROR)

    discovery_up = [r for r in discovery if is_up(r)]
    discovery_down = [r for r in discovery if is_down(r)]
    signal_down = [r for r in signals if is_down(r)]

    if len(discovery_down) == len(discovery):
        return RunStatus.CHANNEL_DOWN
    if discovery_down or signal_down:
        return RunStatus.PARTIAL
    if discovery_up:
        return RunStatus.SUCCESS
    return RunStatus.ERROR


def validate_brief(payload: dict[str, Any]) -> list[str]:
    """Return list of validation errors (empty ⇒ publishable)."""
    errors: list[str] = []
    for key in BRIEF_REQUIRED_FIELDS:
        if key not in payload:
            errors.append(f"missing required field: {key}")
            continue
        value = payload[key]
        if key == "evidence_links":
            if not isinstance(value, list) or not value:
                errors.append("evidence_links must be a non-empty list")
            elif not all(isinstance(x, str) and x.strip() for x in value):
                errors.append("evidence_links entries must be non-empty strings")
        else:
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{key} must be a non-empty string")

    do_value = payload.get("do", "")
    if isinstance(do_value, str) and do_value.strip():
        action = do_value.strip().split(None, 1)[0] if do_value.strip() else ""
        # Allow "观望：理由" or "观望 — 理由" or "观望 理由"
        prefix = None
        for allowed in DO_ALLOWED:
            if do_value.strip().startswith(allowed):
                prefix = allowed
                break
        if prefix is None:
            errors.append(f"do must start with one of {DO_ALLOWED}")

    claim = payload.get("claim", "")
    if isinstance(claim, str) and len(claim) > 150:
        errors.append("claim must be ≤150 Chinese/Latin characters for scannability")

    fake = payload.get("fake_demand", "")
    if fake is not None and not isinstance(fake, str):
        errors.append("fake_demand must be a string when present")

    return errors


def status_reader_copy(status: ChannelStatus) -> str:
    """Human copy for Digest pipeline-health block — never confuse down with empty."""
    if status == ChannelStatus.SUCCESS:
        return "正常，有候选"
    if status == ChannelStatus.EMPTY:
        return "正常，本通道无新命中（≠领域静默）"
    if status == ChannelStatus.UNAVAILABLE:
        return "不可用（≠零候选；勿写成「本周无新闻」）"
    return "错误（≠零候选）"
