# Radar Confidence and Review Theme Design

## Purpose

Make daily discovery auditable without confusing keyword recall with inclusion
confidence, and make deep-review pages easier to scan without exposing the internal
role-weight recipe.

## Discovery and Inclusion Flow

1. `find_arxiv_candidates.py` queries the official arXiv Export API and records the
   endpoint and its role in every output payload.
2. Each hit receives a conservative discovery confidence based on title and abstract
   evidence. This score is triage metadata only.
3. Every candidate remains marked for manual inclusion review. The maintainer checks
   primary-source metadata, world-model centrality, contribution type, and whether the
   work is a single-method paper.
4. Accepted entries use `verified_public_source` and an explicit inclusion rationale.
5. `select_review_target.py` filters out entries that lack verified status, canonical
   source URL, complete metadata, recognized relevance, rationale, or a qualifying
   overview/framing paper type before ranking value.

## Review Page Organization

The visible percentage/role recipe is removed. Each deep review follows the source
paper's own major sections and terminology first. For OpenWorldLib, the visible
modules are definition and related tasks, framework design, discussion, evaluation,
and conclusion.

Executive, architecture, domain, implementation, and research backgrounds still
shape the questions, critiques, and implications inside those modules, but they do
not appear as reader-facing themes. In particular, product/strategy and engineering
governance are not standalone sections; relevant insights are placed under the
paper's discussion, evaluation, limitations, or conclusion sections.

## Failure Handling

- Network errors leave the existing candidate library untouched.
- Medium- and low-confidence discoveries remain reviewable but cannot bypass the
  primary-source gate.
- A paper that fails any selection-confidence check is excluded from automated target
  ranking.
- Feishu upload failures remain explicit and do not block repository validation.

## Verification

- Unit tests cover World Action Model phrasing, single-method false positives,
  canonical URL enforcement, and paper-type enforcement.
- The selector prints every confidence check in its JSON result.
- Paper validation, review-manifest generation, UTF-8 parsing, required theme markers,
  and `git diff --check` run before delivery.
