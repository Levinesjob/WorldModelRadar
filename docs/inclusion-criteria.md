# Inclusion Criteria

This repository tracks overview-style papers about world models from 2026 onward.

## Date Window

- Start date: 2026-01-01
- Current cutoff: 2026-07-14
- The date used is the public arXiv/public-source submission date unless a peer-reviewed
  publication date is clearly more appropriate.

## Included

A paper can be included when it satisfies both:

1. It is publicly discoverable and has a stable paper page.
2. It is an overview-style work, or a close substitute, about world models:
   survey, review, roadmap, taxonomy, position, critique, definition, framework, or
   systematic comparison.

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
