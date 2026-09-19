"""Adapter protocol and runner utilities."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from radar.http_util import HttpError
from radar.schemas import ChannelResult, ChannelStatus, Signal


@dataclass
class AdapterContext:
    """Shared run context passed to every adapter."""

    use_fixtures: bool = False
    fixtures_dir: Path | None = None
    timeout: float = 30.0
    max_results: int = 25
    github_token: str | None = None
    known_arxiv_ids: set[str] | None = None


class Adapter(ABC):
    name: str
    role: str  # discovery | signal
    endpoint: str = ""

    @abstractmethod
    def discover(self, ctx: AdapterContext) -> list[Signal]:
        """Return signals. Raise HttpError or Exception on hard failure."""

    def fixture_file(self, ctx: AdapterContext, filename: str) -> Path | None:
        if not ctx.use_fixtures or ctx.fixtures_dir is None:
            return None
        path = ctx.fixtures_dir / filename
        return path if path.exists() else None


def run_adapter(adapter: Adapter, ctx: AdapterContext) -> ChannelResult:
    """Execute one adapter with isolation; never raises to caller."""
    started = time.perf_counter()
    try:
        signals = adapter.discover(ctx)
        duration_ms = int((time.perf_counter() - started) * 1000)
        status = ChannelStatus.SUCCESS if signals else ChannelStatus.EMPTY
        return ChannelResult(
            channel=adapter.name,
            role=adapter.role,
            status=status,
            item_count=len(signals),
            signals=signals,
            message="ok" if signals else "no matches (channel healthy)",
            duration_ms=duration_ms,
            endpoint=adapter.endpoint,
        )
    except HttpError as exc:
        duration_ms = int((time.perf_counter() - started) * 1000)
        return ChannelResult(
            channel=adapter.name,
            role=adapter.role,
            status=ChannelStatus.UNAVAILABLE,
            item_count=0,
            error_code=exc.code,
            message=exc.message,
            duration_ms=duration_ms,
            endpoint=adapter.endpoint,
        )
    except Exception as exc:  # noqa: BLE001 — isolation boundary
        duration_ms = int((time.perf_counter() - started) * 1000)
        return ChannelResult(
            channel=adapter.name,
            role=adapter.role,
            status=ChannelStatus.ERROR,
            item_count=0,
            error_code="adapter_error",
            message=str(exc),
            duration_ms=duration_ms,
            endpoint=adapter.endpoint,
        )


def run_adapters_parallel(
    adapters: list[Adapter],
    ctx: AdapterContext,
    *,
    max_workers: int = 5,
) -> list[ChannelResult]:
    """Run adapters in parallel; one failure never stops others."""
    results: list[ChannelResult] = []
    if not adapters:
        return results

    with ThreadPoolExecutor(max_workers=min(max_workers, len(adapters))) as pool:
        futures = {pool.submit(run_adapter, adapter, ctx): adapter for adapter in adapters}
        for future in as_completed(futures):
            results.append(future.result())

    # Stable order: discovery first by declared order, then signals.
    order = {a.name: i for i, a in enumerate(adapters)}
    results.sort(key=lambda r: order.get(r.channel, 999))
    return results


def failing_adapter(
    name: str,
    role: str,
    exc: Exception,
) -> Adapter:
    """Test helper: adapter that always raises."""

    class _Fail(Adapter):
        def discover(self, ctx: AdapterContext) -> list[Signal]:
            raise exc

    adapter = _Fail()
    adapter.name = name
    adapter.role = role
    adapter.endpoint = "test://fail"
    return adapter


def ok_adapter(name: str, role: str, signals: list[Signal] | None = None) -> Adapter:
    """Test helper: adapter that returns signals (or empty)."""
    payload = list(signals or [])

    class _Ok(Adapter):
        def discover(self, ctx: AdapterContext) -> list[Signal]:
            return list(payload)

    adapter = _Ok()
    adapter.name = name
    adapter.role = role
    adapter.endpoint = "test://ok"
    return adapter
