# Radar Content System

WorldModel Radar is not an awesome list. It is a living intelligence map for
people who need to understand where world-model research is moving, what is
real, what is still speculative, and where useful work can be done.

The operating principle is:

1. Content first.
2. Presentation second.
3. Promotion last.

The repository should earn attention because the radar helps people think better,
not because it packages weak content nicely.

## Target Readers

The radar serves four reader groups. They overlap, but each reads for a different
decision.

| Reader | Decision They Need To Make | What The Radar Should Give Them |
| --- | --- | --- |
| AI founders and product leaders | Which world-model opportunities are real enough to explore? | Opportunity maps, fake-demand warnings, user pain, adoption timing, domain wedges. |
| Architects and engineering leaders | What would a working system require? | Data contracts, model interfaces, evaluation loops, cost, scaling limits, migration paths. |
| Researchers and PhD students | Where are the open research problems? | Taxonomies, unresolved bottlenecks, benchmark gaps, falsifiable hypotheses, related work maps. |
| Strategy analysts and investors | Which parts may become infrastructure or platforms? | Maturity curves, ecosystem signals, code/repo momentum, discussion heat, risk boundaries. |

## Depth Ladder

Every reader should be able to enter at the right depth and go deeper without
getting lost.

| Layer | Reader Question | Artifact |
| --- | --- | --- |
| 1. Scan | What changed recently? | Weekly radar summary, newest papers, discussion signals. |
| 2. Map | Where does this paper sit in the field? | Domain map, taxonomy position, adjacent papers, open clusters. |
| 3. Deep Read | What is the paper really saying? | Structured HTML review with thesis, architecture, opportunity, risks, and limits. |
| 4. Decision | What should I do with this? | Builder/research/strategy takeaways, real problems vs fake demand, migration path. |
| 5. Watchlist | What should be monitored next? | Follow-up papers, repos, benchmarks, authors, labs, and debates. |

The shallow layers are for speed. The deep layers are where the repository earns
trust.

## Source Funnel

The radar should not rely only on arXiv search. arXiv remains the canonical paper
source for many entries, but candidate discovery should combine primary sources,
code signals, and international discussion signals.

| Source Class | Examples | What It Contributes | How To Use It |
| --- | --- | --- | --- |
| Primary paper sources | arXiv, OpenReview, conference pages, journal pages, lab publication pages | Stable metadata and paper text | Required for inclusion. |
| Code and artifact sources | GitHub, Hugging Face, Papers with Code, project pages | Implementation maturity, reproducibility, ecosystem momentum | Raises priority and informs engineering analysis. |
| Discussion sources | X/Twitter, Hacker News, Reddit ML communities, LessWrong/Alignment Forum, technical blogs, newsletters | Attention, controversy, practitioner pain, emerging terminology | Candidate priority signal only, never standalone proof. |
| Lab and company sources | Meta AI/FAIR, Google DeepMind, NVIDIA, Tesla AI, OpenAI, Microsoft Research, university labs | Strategic direction, benchmark releases, tooling, institutional framing | Useful for trend context and watchlists. |
| Community collections | Awesome lists, GitHub topic pages, curated reading lists | Discovery of adjacent papers and repos | Useful for recall, but must be verified against primary sources. |

## Discussion Signal Policy

Discussion heat is useful because it reveals what the community is actually
arguing about. It is dangerous because it can reward hype. The radar should treat
discussion as a triage signal.

A paper becomes a higher-priority candidate when at least one of these is true:

- Multiple credible researchers or builders discuss it independently.
- Its GitHub repository gains meaningful stars, forks, issues, or external reuse.
- It appears in respected newsletters, reading groups, conference workshops, or
  lab discussions.
- It triggers disagreement about definitions, evaluation, safety, economics,
  embodied action, or real-world deployment.
- It introduces a reusable benchmark, framework, dataset, codebase, or taxonomy.

A paper should not be prioritized just because:

- The title is trendy.
- A single viral post mentions it.
- It has a flashy demo without a clear evaluation boundary.
- It is a method paper with no survey, roadmap, taxonomy, framework, or field-level
  contribution.

## Review Contract

Each deep review should answer the same reader-facing questions while respecting
the source paper's own structure.

Required content:

- Core thesis: what changed if this paper is right?
- Field position: which part of the world-model map does it affect?
- Real problem: what pain, bottleneck, or missing infrastructure does it address?
- Fake demand: what tempting but weak interpretation should readers avoid?
- Architecture: data, state, action, transition, evaluation, deployment, feedback.
- Maturity: research idea, prototype, benchmark, codebase, early product, platform.
- Cost and complexity: data cost, training/inference cost, evaluation cost,
  operational cost, organizational complexity.
- Migration path: how a team could move from today's systems toward this direction.
- Open questions: what remains unproven and what would falsify the thesis?
- Watchlist: authors, labs, repos, benchmarks, debates, and adjacent papers to track.

## Radar Scores

Scores should explain why a paper matters, not pretend to be objective truth.

Suggested dimensions:

| Score | Meaning |
| --- | --- |
| Field Signal | How strongly the paper clarifies or changes the field map. |
| Discussion Heat | How much credible external discussion exists. |
| Implementation Grounding | Whether code, benchmarks, datasets, or reproducible artifacts exist. |
| Opportunity Surface | How many real builder/research/product opportunities it exposes. |
| Maturity | How close the idea is to being operationally usable. |
| Risk / Uncertainty | How much remains unverified, unsafe, costly, or underspecified. |

The score should always include short evidence notes and source links.

## Weekly Big Picture

The weekly big picture should synthesize movement, not just list reviewed papers.

It should include:

- What changed this week.
- Which cluster gained signal.
- Which debates are emerging.
- Which assumptions weakened.
- Which opportunities became more concrete.
- Which papers moved onto the watchlist because of discussion heat.
- Which open problems are now more important than before.

The weekly page is the main reader experience. Individual reviews are the evidence.

## Editorial Rule

Never let presentation outrun content. A beautiful page with weak judgment damages
the radar. A plain page with sharp synthesis is still valuable.
