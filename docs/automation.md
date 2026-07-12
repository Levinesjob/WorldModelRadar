# Local Daily Automation

WorldModel Radar can be maintained by a local Codex cron automation that runs once
per day against this repository.

## What The Automation Does

1. Pull the latest `main` branch from GitHub.
2. Search arXiv for 2026+ candidate papers related to world models.
3. Compare candidates with `data/papers.json`.
4. Promote only papers that satisfy `docs/inclusion-criteria.md`.
5. Re-render the README quick-view table.
6. Validate metadata.
7. Commit and push changes only when the canonical paper list or documentation changes.

## Local Commands

Run candidate discovery:

```bash
python scripts/find_arxiv_candidates.py
```

Rebuild README after editing `data/papers.json`:

```bash
python scripts/render_readme.py
```

Validate metadata:

```bash
python scripts/validate_papers.py
```

## Notes

- `data/candidates/*.json` is ignored by Git because it is a local working cache.
- The automation should not commit a daily empty update.
- The automation should keep borderline papers in `docs/search-log.md` instead of
  adding them to the canonical list.
