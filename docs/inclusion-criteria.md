# Inclusion Criteria

This repository tracks overview-style papers about world models from 2026 onward.

## Date Window

- Start date: 2026-01-01
- Current cutoff: 2026-07-17
- The date used is the public arXiv/public-source submission date unless a peer-reviewed
  publication date is clearly more appropriate.

## Included

A paper can be included when it satisfies both:

1. It is publicly discoverable and has a stable paper page.
2. It is an overview-style work, or a close substitute, about world models:
   survey, review, roadmap, taxonomy, position, critique, definition, framework, or
   systematic comparison.

## High-Confidence Gate

Search hits are candidates, not accepted papers. A paper enters `data/papers.json`
only after a maintainer verifies all of the following:

1. The title, authors, first-public date, abstract, and canonical URL agree with a
   primary public source such as the official arXiv abstract page or publisher page.
2. World models are central to the paper's stated contribution, not merely a module,
   keyword, application detail, or benchmark target.
3. The paper makes a genuine overview or framing contribution: survey, review,
   roadmap, taxonomy, definition, position, critique, reusable framework, or
   systematic comparison.
4. The abstract and, when necessary, full text are checked to rule out a single-method
   paper whose title or abstract happens to contain words such as `framework`,
   `benchmark`, or `challenges`.
5. `why_included`, `paper_type`, `relevance`, and `status` record the decision. Only
   entries marked `verified_public_source` are eligible for automated deep-review
   selection.

The discovery script's `discovery_confidence` describes keyword evidence only. It
never replaces this manual primary-source gate.

### Discovery Confidence Levels

| Level | Automated evidence | Meaning |
| --- | --- | --- |
| `high` | A world-model family phrase and an overview/framing term both appear in the title. | Strong candidate for immediate primary-source review; not automatic acceptance. |
| `medium` | A world-model family phrase appears in the title and an overview/framing term appears in the abstract. | Likely relevant, but commonly includes single-method false positives. |
| `low` | The broad query and text filters match, but title evidence is incomplete. | Recall-only lead; requires careful centrality and contribution checks. |

Discovery recognizes `world model(s)`, `world modeling/modelling`, hyphenated forms,
`world action model(s)`, and `world foundation model(s)`.

### Formal Inclusion and Selection Confidence

Formal confidence is pass/fail rather than a soft score. All six checks must pass:

- `verified_public_source`
- canonical public URL matching the arXiv id when present
- complete title, authors, date, and source metadata
- explicit `why_included` rationale
- recognized `core`, `domain`, or `adjacent` relevance
- survey/review/roadmap/taxonomy/definition/framework/position/perspective/critique type

## Relevance Labels

- `core`: world models are the central subject.
- `domain`: world models are central inside a specific domain, such as robotics,
  healthcare, edge intelligence, or code intelligence.
- `adjacent`: world models are important but not the paper's only or primary subject.

## Excluded By Default

- Method papers that introduce a single world-model architecture without a substantial
  survey, taxonomy, or framing contribution.
- Broad AI-agent, video-generation, robotics, or embodied-AI surveys that only mention
  world models as one component.
- Pre-2026 surveys, even if important background.

## Borderline Handling

Borderline papers can stay in `data/papers.json` only when their `relevance` is
`adjacent` and `why_included` states the reason plainly. Otherwise, record them in
`docs/search-log.md` as excluded or background.
