"""CLI entry for Radar Runtime."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from radar.brief import seed_briefs_from_papers
from radar.paths import BRIEFS_DIR, PAPERS_FILE
from radar.runtime import load_papers, run_pipeline
from radar.schemas import validate_brief


def cmd_run(args: argparse.Namespace) -> int:
    artifacts = run_pipeline(
        use_fixtures=args.fixtures,
        include_signals=not args.discovery_only,
        seed_briefs=not args.skip_seed_briefs,
        write_digest_files=not args.skip_digest,
        max_results=args.max_results,
        judgment=args.judgment,
    )
    summary = {
        "run_id": artifacts.run_id,
        "status": artifacts.status.value,
        "candidate_count": artifacts.candidate_count,
        "brief_count": artifacts.brief_count,
        "run_manifest": str(artifacts.run_manifest_path),
        "triage": str(artifacts.triage_path),
        "digest_md": str(artifacts.digest_md) if artifacts.digest_md else None,
        "channels": [
            {
                "channel": r.channel,
                "role": r.role,
                "status": r.status.value,
                "item_count": r.item_count,
                "error_code": r.error_code,
            }
            for r in artifacts.channel_results
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if artifacts.status.value == "channel_down":
        return 2
    return 0


def cmd_seed_briefs(_args: argparse.Namespace) -> int:
    papers = load_papers(PAPERS_FILE)
    written, errors = seed_briefs_from_papers(papers, BRIEFS_DIR)
    print(json.dumps({"written": written, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def cmd_validate_brief(args: argparse.Namespace) -> int:
    payload = json.loads(Path(args.path).read_text(encoding="utf-8"))
    errors = validate_brief(payload)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m radar",
        description="WorldModelRadar Runtime — discovery → triage → brief → digest",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run one full pipeline pass")
    run.add_argument(
        "--fixtures",
        action="store_true",
        help="Use offline fixtures under data/fixtures (no network)",
    )
    run.add_argument(
        "--discovery-only",
        action="store_true",
        help="Skip optional signal adapters (HN, HF)",
    )
    run.add_argument("--skip-seed-briefs", action="store_true")
    run.add_argument("--skip-digest", action="store_true")
    run.add_argument("--max-results", type=int, default=25)
    run.add_argument("--judgment", type=str, default=None, help="Override Digest one-line judgment")
    run.set_defaults(func=cmd_run)

    seed = sub.add_parser("seed-briefs", help="Generate Chinese briefs from data/papers.json")
    seed.set_defaults(func=cmd_seed_briefs)

    validate = sub.add_parser("validate-brief", help="Validate a brief JSON file")
    validate.add_argument("path", type=str, help="Path to brief JSON")
    validate.set_defaults(func=cmd_validate_brief)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
