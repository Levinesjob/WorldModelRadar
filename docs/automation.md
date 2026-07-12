# Local Automation

WorldModel Radar is maintained by a local Codex cron automation that runs once
per day at local midnight against this repository.

## What The Automation Does

1. Pull the latest `main` branch from GitHub.
2. Search arXiv for 2026+ candidate papers related to world models.
3. Compare candidates with `data/papers.json`.
4. Promote only papers that satisfy `docs/inclusion-criteria.md`.
5. Re-render the README quick-view table.
6. Validate metadata.
7. Select the highest-value paper for deep reading:
   - if the current run adds qualified papers, choose the strongest new paper;
   - otherwise choose the strongest existing paper that does not yet have an HTML review;
   - if all papers already have reviews, refresh the highest-impact existing review.
8. Generate or refresh one deep-read HTML in `docs/reviews/`, using
   `docs/reviews/a-definition-roadmap-world-models.html` as the canonical template.
9. Update `docs/reviews/reviews.json` and, once per week, regenerate
   `docs/reviews/world-model-big-picture.html`.
10. Send the generated HTML file to Feishu chat
    `oc_ab3da5be78816bc84a94449b371fa1ca`.
11. Commit and push changes only when the canonical paper list, review HTML,
    review manifest, big-picture page, or documentation changes.

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

Select the next deep-read target:

```bash
python scripts/select_review_target.py
```

When the daily run adds new papers, pass the new paper ids or arXiv ids:

```bash
python scripts/select_review_target.py --prefer-id 2607.06401
```

Rebuild the review manifest after adding or refreshing an HTML review:

```bash
python scripts/build_review_manifest.py
```

Build the weekly big-picture HTML:

```bash
python scripts/build_big_picture.py
```

Send an HTML file to the configured Feishu chat:

```bash
python scripts/send_feishu_file.py docs/reviews/a-definition-roadmap-world-models.html
```

For a local smoke test that does not call Feishu:

```bash
python scripts/send_feishu_file.py docs/reviews/a-definition-roadmap-world-models.html --dry-run
```

## Notes

- `data/candidates/*.json` is ignored by Git because it is a local working cache.
- The automation should not commit a daily empty update.
- The automation should keep borderline papers in `docs/search-log.md` instead of
  adding them to the canonical list.
- Feishu credentials must stay outside the repository. The sender reads either
  `FEISHU_APP_ID` and `FEISHU_APP_SECRET`, or the local
  `~/.openclaw-autoclaw/openclaw.json` file.
- Review HTML files should include `worldmodel-radar:*` meta tags so
  `scripts/build_review_manifest.py` can track which papers have been reviewed.
