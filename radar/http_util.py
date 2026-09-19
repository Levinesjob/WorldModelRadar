"""Minimal HTTP helpers with fixture override for offline runs."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


class HttpError(Exception):
    def __init__(self, code: str, message: str, http_status: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.http_status = http_status


def fetch_bytes(
    url: str,
    *,
    timeout: float = 30.0,
    headers: dict[str, str] | None = None,
    fixture_path: Path | None = None,
) -> bytes:
    if fixture_path is not None:
        return fixture_path.read_bytes()

    req_headers = {"User-Agent": "WorldModelRadar/0.1 (+https://github.com/Levinesjob/WorldModelRadar)"}
    if headers:
        req_headers.update(headers)
    request = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        code = "http_429" if exc.code == 429 else f"http_{exc.code}"
        raise HttpError(code, f"HTTP {exc.code} for {url}", http_status=exc.code) from exc
    except urllib.error.URLError as exc:
        raise HttpError("network_error", f"network error for {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise HttpError("timeout", f"timeout for {url}") from exc


def fetch_text(
    url: str,
    *,
    timeout: float = 30.0,
    headers: dict[str, str] | None = None,
    fixture_path: Path | None = None,
    encoding: str = "utf-8",
) -> str:
    return fetch_bytes(url, timeout=timeout, headers=headers, fixture_path=fixture_path).decode(encoding)


def fetch_json(
    url: str,
    *,
    timeout: float = 30.0,
    headers: dict[str, str] | None = None,
    fixture_path: Path | None = None,
) -> Any:
    text = fetch_text(url, timeout=timeout, headers=headers, fixture_path=fixture_path)
    return json.loads(text)
