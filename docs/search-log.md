# Search Log

Last checked: 2026-09-01

## Queries Used

- `2026 world models survey arxiv review paper "world models"`
- `site:arxiv.org/abs/26 "world model" "survey"`
- `site:arxiv.org/abs/26 "world models" "survey"`
- `site:arxiv.org/abs/26 "world model" "review"`
- `site:arxiv.org/abs/26 "world model" "roadmap"`
- `site:arxiv.org/abs/26 "world model" "taxonomy"`
- `site:arxiv.org/abs/26 "world models" "future directions"`
- `site:arxiv.org/abs/26 "world model" "position paper"`
- `site:arxiv.org/abs/26 "robot" "world model" "survey"`
- `site:arxiv.org/abs/26 "medical world models"`
- `site:arxiv.org/abs/26 "world modelling" "code" "survey"`

## Public Sources Checked

- arXiv abstract pages
- arXiv experimental HTML full text
- Web search snippets for public paper metadata
- Paper-linked GitHub repositories when present in abstracts

## 2026-09-01 Discovery Notes

- Canonical Scout could not complete because the second configured primary-paper
  request to the arXiv Export API returned HTTP 429. It produced no new
  `latest.json`, so this run does not report an empty candidate set and does not
  advance the inclusion cutoff. The 2026-08-28 candidate file remains a stale
  prior-run artifact rather than evidence about 2026-09-01.
- Channel status: arXiv `unavailable` (HTTP 429); Hacker News, Reddit, X/Twitter,
  and GitHub `unavailable` because Scout stopped before those configured channels
  ran. These states are not evidence of no papers, discussion, or implementation.
- With no valid current-run candidate input, the selector chose existing
  unreviewed paper `2601.07823`, *Video Generation Models in Robotics --
  Applications, Research Challenges, Future Directions*. Official arXiv abstract
  and full HTML verification confirmed its implicit/explicit video-world-model
  distinction, four-part robotics application map, evaluation mismatch between
  perceptual quality and task utility, and ten deployment challenges spanning
  physics, uncertainty, control, safety, horizon, data, and compute.

## 2026-08-29 Discovery Notes

- Canonical Scout could not complete because the first configured primary-paper
  request to the arXiv Export API returned HTTP 429. It produced no new
  `latest.json`, so this run does not report an empty candidate set and does not
  advance the inclusion cutoff. The 2026-08-28 candidate file remains a prior-run
  artifact rather than evidence about 2026-08-29.
- Channel status: arXiv `unavailable` (HTTP 429); Hacker News, Reddit, X/Twitter,
  and GitHub `unavailable` because Scout stopped before those configured channels
  ran. These states are not evidence of no papers, discussion, or implementation.
- With no valid new-candidate input, the selector chose existing unreviewed paper
  `2606.23690`, *Beyond the Autoregressive Horizon: A Comprehensive Survey of
  Diffusion Models, World Modelling, and State Space Models for Code*. Official
  arXiv abstract and full HTML verification confirmed its three-paradigm map,
  execution-trace and agent-interaction account of Code World Models, fragmented
  cross-paradigm benchmark landscape, hybrid-architecture thesis, and stated
  limitation that the paradigms cannot yet be compared on one standardized
  benchmark.

## 2026-08-28 Discovery Notes

- Canonical Scout produced 16 merged candidates and an eight-item shortlist. The
  arXiv overview queries contributed six candidates; ten additional candidates
  came from discussion-discovered arXiv ids after known-paper filtering. Only the
  shortlist and any `credible` or `strong` heat were passed to inclusion review.
  No paper reached credible discussion heat, and no new paper passed the
  field-level inclusion gate.
- Official arXiv abstracts confirmed that the two newly assessed world-model
  shortlist papers are single systems. ConfAL-WM (`2608.25572`) adds a dense
  confidence probe and task/frame/patch active-learning pipeline to EVAC for
  post-training on RoboTwin2.0. Code World Model (`2608.25927`) combines a coding
  agent, executable persistent state, a proxy video representation, and a
  fine-tuned video renderer. Both expose useful implementation hypotheses, but
  neither is a survey, taxonomy, roadmap, position, critique, or reusable
  field-level framework, so neither was placed in the main list.
- GaussianWAM (`2608.24714`) and Game2World Engine (`2608.24680`) reappeared and
  retain the 2026-08-27 single-method/system decisions. The remaining four
  shortlist entries (`2608.23228`, `2608.21560`, `2608.20186`, and `2608.15089`)
  were Hacker News-discovered papers on a linker, TESS planet validation, EEG
  decoding, and an agent harness rather than world models. Two low-confidence
  arXiv-query hits (`2608.25666`, `2608.24534`) were also subject false positives.
- Channel status: arXiv `ok`; Hacker News `ok` (20 exact arXiv-link hits, with no
  credible or strong world-model-paper heat); GitHub `empty` (channel ran, zero
  exact implementation hits); Reddit `unauthorized` (HTTP 403); X/Twitter
  `unauthorized` (HTTP 402). Unavailable channels were not interpreted as no
  discussion.
- With no new inclusion, the selector chose `2606.06556`, *Robots Need More than
  VLA and World Models*, for deep reading. Official arXiv abstract and full HTML
  verification confirmed its grounding-centric robotics thesis and four missing
  components: physical data engines, task-preserving retargeting, physics-grounded
  consequence models, and task-conditioned reward/deployment loops.

## 2026-08-27 Discovery Notes

- Canonical Scout produced 18 merged candidates and an eight-item shortlist. The
  arXiv overview queries contributed eight candidates; ten additional candidates
  came from discussion-discovered arXiv ids after known-paper filtering. Only the
  shortlist and any `credible` or `strong` heat were passed to inclusion review.
  No paper reached credible discussion heat, and no new paper passed the
  field-level inclusion gate.
- Official arXiv abstracts confirmed that the two newly assessed shortlist papers
  are useful but narrow systems. GaussianWAM (`2608.24714`) distills geometry and
  semantics from a 3D Gaussian field into existing WAM representations during
  training, then removes the teachers and auxiliary path at deployment.
  Game2World Engine (`2608.24680`) contributes a gameplay-UI taxonomy, a paired
  UI-removal dataset and data engine, and the GameCleaner model. Neither paper is
  a survey, review, roadmap, position, or reusable field-level framework, so they
  were not placed in the main list.
- GeoWAM (`2608.23486`) and Future Querying (`2608.23248`) reappeared in the
  shortlist and retain the 2026-08-26 single-method decisions. The other four
  shortlist entries (`2608.21590`, `2608.20186`, `2608.15089`, and `2608.02859`)
  were Hacker News-discovered papers on black-hole singularities, EEG decoding,
  agent harness scaling, and AI-generated mathematics rather than world models.
- Channel status: arXiv `ok`; Hacker News `ok` (18 exact arXiv-link hits, with no
  credible or strong world-model-paper heat); Reddit `unauthorized` (HTTP 403);
  X/Twitter `unauthorized` (HTTP 402); GitHub `unauthorized` (HTTP 403). The three
  unavailable channels were not interpreted as evidence of no discussion or no
  implementation.

## 2026-08-26 Discovery Notes

- Canonical Scout produced 17 merged candidates and an eight-item shortlist. The
  arXiv overview queries contributed seven candidates; discussion discovery
  contributed ten arXiv ids. Only the shortlist and any `credible` or `strong`
  heat were passed to inclusion review. No paper reached credible discussion
  heat, and no new paper passed the field-level inclusion gate.
- Four shortlist papers were genuine world-model candidates but remained
  single-method or single-system contributions: MOSH-WM (`2608.22750`) proposes
  one object-centric soft-Hamiltonian architecture; GeoWAM (`2608.23486`)
  proposes one geometry-prediction driving WAM; Future Querying (`2608.23248`)
  introduces and evaluates one endpoint-agnostic clinical-query framework; and
  DreamMimic (`2608.22278`) uses one RSSM-assisted humanoid-policy distillation
  pipeline. Their official arXiv abstracts do not provide a survey, taxonomy,
  roadmap, position, or reusable field-level framework.
- The other four shortlist entries (`2608.20186`, `2608.16884`, `2608.15089`,
  and `2608.02859`) came from exact arXiv links in Hacker News results but concern
  EEG decoding, matrix-multiplication optimization, agent harness scaling, and
  AI-generated mathematics. They are not world-model papers. This is useful
  evidence that discussion-discovered ids still require subject-centrality
  screening before curation.
- Channel status: arXiv `ok`; Hacker News `ok` (17 exact arXiv-link hits, none
  constituting credible world-model-paper heat); GitHub `empty` (channel ran,
  zero exact implementation hits); Reddit `unauthorized` (HTTP 403); X/Twitter
  `unauthorized` (HTTP 402 for recent search). Unavailable channels were not
  interpreted as no discussion.
- With no new inclusion, the selector chose the existing medical-world-model
  review (`2606.16721`) for deep reading. Official arXiv HTML confirmed its
  patient-state / clinical-dynamics / intervention-support roadmap, its serial /
  shared-state / closed-loop composition taxonomy, and its warning that
  plausible rollouts are not causal or clinical decision evidence.

## 2026-08-23 Discovery Notes

- The official arXiv Export API returned four candidates, all previously
  assessed on 2026-08-21 or 2026-08-22: RMWorld (`2608.20126`), the
  planning-oriented end-to-end driving survey (`2608.20111`), Orthogonal JEPA
  (`2608.20065`), and DA-WAM (`2608.19085`). No new candidate required an
  inclusion decision, so no paper was added and no empty paper-library update
  was recorded.
- Exact arXiv-id GitHub searches again returned zero repositories. Hacker News
  search counts were inspected hit by hit and were numeric near-matches rather
  than exact paper discussions. Reddit public search returned HTTP 403, so it
  remains an unavailable channel rather than evidence of no discussion. A
  third-party summary and a bulk discussion-board paper list for Orthogonal
  JEPA were not treated as credible independent heat.
- The selected existing position paper `2602.01630` was verified against its
  official arXiv abstract and full HTML. The same lead-author community's
  follow-on OpenWorldLib repository had 860 stars and 52 forks in the
  2026-08-23 retrieval snapshot and was pushed on 2026-08-23. This is a useful
  implementation/ecosystem continuation of the modular thesis, but it is not
  presented as the position paper's own validated implementation.

## 2026-08-22 Discovery Notes

- The official arXiv Export API returned four candidates. DA-WAM
  (`2608.19085`) had already been assessed on 2026-08-21; the three newly
  assessed candidates were RMWorld (`2608.20126`), the planning-oriented
  end-to-end driving survey (`2608.20111`), and Orthogonal JEPA
  (`2608.20065`). Official arXiv metadata and full abstracts were used for the
  inclusion decisions. None passed the radar's overview or field-level framing
  gate, so no paper was added.
- Exact arXiv-id searches returned no GitHub repositories for the three new
  candidates. Hacker News results were numeric near-matches rather than exact
  paper discussions. Reddit public search returned HTTP 403, so that channel is
  recorded as unavailable rather than as evidence of no discussion. No
  implementation or discussion signal changed the inclusion decisions.
- The selected existing survey `2606.01164` was verified against its official
  arXiv HTML. Its author-maintained repository had 213 stars and 14 forks in the
  2026-08-22 retrieval snapshot and was pushed on 2026-08-20. This is a useful
  curation and ecosystem-maintenance signal, not proof that the surveyed systems
  share an implementation or production maturity level.

## 2026-08-21 Discovery Notes

- The official arXiv Export API returned five candidates. Four had already been
  assessed on 2026-08-20; the only newly assessed candidate was DA-WAM
  (`2608.19085`). Its official arXiv abstract describes one decision-aligned
  driving architecture that jointly trains predictive future latents and
  trajectory scoring on NAVSIM, rather than a survey, taxonomy, roadmap,
  definition, position, or field-level framework. No paper was added.
- Exact-title and arXiv-id searches found no author-official DA-WAM code or
  project page and no credible independent Hacker News, Reddit, or X/Twitter
  discussion signal. This absence is recorded only as a priority signal, not as
  evidence against the method.
- Primary-source review of the selected existing survey `2605.00080` confirmed
  its author-maintained repository and project page. The repository organizes
  papers, code, models, benchmarks, and datasets by the survey's policy,
  simulator, video-generation, evaluation, and data taxonomy; its URL was added
  to the paper metadata as an implementation/ecosystem signal.

## 2026-08-20 Discovery Notes

- The official arXiv Export API returned four candidates published on August
  17-18. Official arXiv abstract pages were used to verify titles, authors,
  dates, contribution scope, and whether the papers linked author-official
  artifacts. None passed the overview or field-level framing gate, so no paper
  was added to the main table.
- No candidate linked an author-official code or project artifact from its
  arXiv page, GitHub repository search returned no arXiv-id matches, and Hacker
  News full-title/arXiv-id filtering returned no exact discussion hits. Reddit
  public search returned HTTP 403, so this run records it as unavailable rather
  than interpreting it as evidence of no discussion. The AutoGLM browser path
  also failed to initialize its browser extension, so no X/Twitter signal was
  treated as verified.

## 2026-08-14 Discovery Notes

- The official arXiv Export API returned HTTP 429 after network access was
  granted, so this run did not interpret an empty response as an empty candidate
  set. The official arXiv search page was used as a primary-source fallback and
  produced 13 newly assessed candidates under the repository's equivalent
  world-model plus overview/framing keyword gate.
- Added `How Can Driving World Models Do Counterfactual Prediction?`
  (`2608.11601`). The paper is a field-level critique and reusable evaluation
  framework: it distinguishes direct action-conditioned prediction from an
  episode-specific counterfactual, formalizes the missing abduction step, and
  tests the distinction with 186 matched CARLA cases across two frozen driving
  world models.
- No author-official code repository or credible independent Hacker News,
  Reddit, or X/Twitter discussion heat was found for the included paper. Purdue
  University and Bosch Center for Artificial Intelligence affiliations are
  retained as an institutional watchlist signal only, not as inclusion evidence.

## 2026-08-11 Discovery Notes

- The official arXiv Export API returned 10 candidates. Five were already
  assessed on 2026-08-10; the five newly assessed API candidates were UniJEPA,
  SimWAM, PILOT, WorldTrace, and TaskSense. Semantic arXiv search added
  WorldClaw and HelloWorld as recall-only leads. None passed the overview or
  field-framing gate, so no paper was added to the main table.
- Implementation and institutional signals were retained only as watchlist
  evidence. SimWAM links an author-official repository with code and weights;
  WorldTrace is listed by an author as an ICML 2026 workshop oral and best-paper
  winner. These signals make the methods worth tracking, but do not turn them
  into surveys, taxonomies, roadmaps, definitions, or field-level frameworks.
- AutoGLM Web Search could not run because the local token service at
  `127.0.0.1:53699` refused the connection. Public web search and official arXiv
  pages were used as fallback. No credible independent Hacker News, Reddit, or
  X/Twitter discussion signal was found for the newly assessed candidates.

## 2026-08-10 Discovery Notes

- The official arXiv Export API candidate script timed out after network access
  was granted, so this run did not interpret an empty response as an empty paper
  set. Web-search fallback was used for recall, followed by official arXiv
  abstract and full-text verification.
- `How Should World Models Be Evaluated for Embodied Decision-Making? A
  Decision-Making-Centric Position` (`2606.15032`) was added after official v2
  verification. It surveys recent evaluation practice, identifies
  claim/evidence mismatch, and contributes an L0-L7 evidential hierarchy plus an
  operational benchmark protocol and evaluation card. No author-official code
  repository was found; third-party indexing and a curated world-model paper
  collection were treated only as weak discovery signals, not inclusion evidence.

## Important Pre-2026 Background Not In Main List

These papers are useful context but fall outside the 2026+ window:

- [Is Sora a World Simulator? A Comprehensive Survey on General World Models and Beyond](https://arxiv.org/abs/2405.03520)
- [Understanding World or Predicting Future? A Comprehensive Survey of World Models](https://arxiv.org/abs/2411.14499)
- [A Survey of World Models for Autonomous Driving](https://arxiv.org/abs/2501.11260)
- [From 2D to 3D Cognition: A Brief Survey of General World Models](https://arxiv.org/abs/2506.20134)
- [A Survey: Learning Embodied Intelligence from Physical Simulators and World Models](https://arxiv.org/abs/2507.00917)
- [A Comprehensive Survey on World Models for Embodied AI](https://arxiv.org/abs/2510.16732)
- [Beyond Generative AI: World Models for Clinical Prediction, Counterfactuals, and Planning](https://arxiv.org/abs/2511.16333)

## Exclusion Notes

- `RMWorld: Task-Aware Radio World Models with Value-of-Information Guided
  Multi-Trial Learning for Multi-UAV Communication Control` (`2608.20126`) was
  not placed in the main list because it proposes one Bayesian residual radio
  world model, acquisition rule, and counterfactual-trial selection pipeline for
  multi-UAV communications. Its risk-reduction framing is useful, but it is a
  single domain method rather than a survey, taxonomy, roadmap, definition, or
  reusable field-level framework.
- `Planning-Oriented End-to-End Autonomous Driving: Architectures, Evaluation,
  and Emerging Paradigms` (`2608.20111`) was not placed in the main list because
  it surveys the broader end-to-end driving field. World-model-based planners
  are one architecture family and world-model validation is one open challenge;
  world models are not the central subject of the survey.
- `Orthogonal JEPA: Factorized Predictive States for Latent World Models`
  (`2608.20065`) was not placed in the main list because it introduces and tests
  one orthogonal predictive-factorization architecture across several domains.
  Cross-domain experiments broaden the method's evidence, but do not make it an
  overview, taxonomy, roadmap, position, or field-level framework.

- `DA-WAM: Decision-Aligned Future Latents for Driving World Models`
  (`2608.19085`) was not placed in the main list because it proposes and
  evaluates one action-conditioned latent predictor and factorized trajectory
  scorer for NAVSIM. The paper exposes a useful causal-conditioning problem,
  but its contribution remains a single driving method rather than an overview
  or reusable field-level framing contribution.

- `Offline Multi-Agent Reinforcement Learning with a Physics-Informed World
  Model for Cooperative Mixed Traffic Control` (`2608.17739`) was not placed in
  the main list because it proposes one physics-informed offline multi-agent RL
  pipeline for a SUMO on-ramp bottleneck. Its interpretable state reconstruction,
  ensemble dynamics, and uncertainty-truncated rollouts are method components,
  not a survey, taxonomy, roadmap, definition, or field-level framework.
- `Electromagnetic World Model for 6G: A Unified Framework for Joint Environment
  Reconstruction and Channel Prediction` (`2608.17769`) was not placed in the
  main list because its “unified framework” is one CSI-plus-RGB architecture,
  dataset, and two-head prediction system for 6G, rather than a reusable
  taxonomy or overview of electromagnetic or general world models.
- `Calibrated Predictive Safety for Heterogeneous Robots: An Action-Conditioned
  JEPA Framework with Model-Based Safety Shields` (`2608.17496`) was not placed
  in the main list because it evaluates one receding-horizon JEPA ranking and
  deterministic shielding pipeline in simulation. The paper explicitly leaves
  real-robot experiments for future work and does not make a field-level review
  or framing contribution.
- `Q-Learning With World Models` (`2608.17163`) was not placed in the main list
  because QWM is a specific test-time imagined-trajectory search method layered
  on standard Q-learning. Avoiding imagined-rollout training bias is a useful
  method signal, but the paper is not an overview, taxonomy, roadmap, position,
  or broadly reusable field framework.

- `H2R-Bench: Benchmarking Human-to-Robot Manipulation Video Generation in
  World Models` (`2608.13049`) was not placed in the main list because it is a
  domain benchmark and model comparison for one cross-embodiment generation
  task, not a survey, taxonomy, roadmap, definition, or field-level framework.
- `The Objective Is the Bottleneck: Latent World Models Encode What Their
  Planners Cannot Use` (`2608.12959`) was not placed in the main list because it
  is a focused reproduction and planner-objective diagnosis on LeWorldModel,
  rather than an overview contribution.
- `HounsWorld: A Multimodal World Model for Hidden Patient-State Readout,
  Reconstruction, and Simulation` (`2608.12904`) was not placed in the main
  list because it introduces one 3B clinical model and HounsBench, not a general
  medical-world-model survey or field framework.
- `BrainWAM: Action-Space Coordination of Semantic Priors and Predictive
  Dynamics for Autonomous Driving` (`2608.12854`) was not placed in the main
  list because it proposes one dual-path driving planner and inference strategy.
- `Scaling Automatic Research Agents via World Models` (`2608.12564`) was not
  placed in the main list because WMRL is a specific post-training method that
  substitutes learned environment execution, rather than an overview of world
  models or their research landscape.
- `MAJEPPA: Morphing and Assessing in a Unified Piano Performance Space`
  (`2608.11026`) was not placed in the main list because it is a piano-performance
  method and a semantic false positive for the radar's learned-world-model scope.
- `R4DSG: Relative 4D Scene Graph Memory for Object-Centric Question Answering
  in Long Egocentric Video` (`2608.11017`) was not placed in the main list
  because it contributes one scene-graph memory architecture, not an overview.
- `ComBodied Agents: a New Paradigm of Human-Centric Agentic AI` (`2608.10915`)
  was not placed in the main list because it frames a broader agent paradigm;
  world models are supporting context rather than the central survey subject.
- `Toward the Cognitive--Physical Limits of Embodied Intelligence through a
  World-Model-Centric Autonomous Racing Agent` (`2608.10618`) was not placed in
  the main list because it presents and evaluates one autonomous-racing system.
- `PBD-AG: Persistent Baseline-Delta Active Graphs with Uncertainty-Aware
  Inspection for Long-Horizon Service Robots` (`2608.10449`) was not placed in
  the main list because it is a specific persistent mapping and inspection
  architecture rather than a field taxonomy or roadmap.
- `Model Discovery Agent: LLM-assisted Bayesian experiment design for
  data-efficient discovery of mechanistic world models` (`2608.09696`) was not
  placed in the main list because it introduces one model-discovery pipeline;
  its mechanistic models are task outputs, not an overview of learned world
  models as an AI field.
- `Sekai2: From World Exploration to Interactive World Modeling` (`2608.09449`)
  was not placed in the main list because it is a dataset release for video-world-
  model pretraining, not a survey, position, taxonomy, or reusable field framework.

- `UniJEPA: A Unified Joint-Embedding Predictive Architecture for Task-Agnostic
  Visual World Modeling` (`2608.07409`) was not placed in the main list because
  it proposes and evaluates one unified JEPA objective and architecture. Its
  comparison of image- and video-level JEPA recipes motivates the method but is
  not a field survey, taxonomy, or roadmap.
- `SimWAM: A Simple World Action Model for End-to-End Autonomous Driving`
  (`2608.07468`) was not placed in the main list because it is a specific
  dual-expert driving planner whose video branch is discarded at inference. Its
  official code and weights are useful implementation signals, not evidence of
  an overview contribution.
- `Decoupling Intention from Trajectory: A Representational Deduction Framework
  for World Action Models` (`2608.06994`) was not placed in the main list because
  the paper's “framework” is the PILOT/RD method for one representation bottleneck,
  rather than a reusable field-level framework or taxonomy.
- `Addressable Memory for Video World Models` (`2608.07408`) was not placed in
  the main list because it contributes the WorldTrace cache method and LoopBench
  for long-horizon visual persistence. The ICML 2026 workshop oral/best-paper
  signal raises watchlist priority but does not change its single-method scope.
- `TaskSense: Focusing on What Matters in World Models` (`2608.06544`) was not
  placed in the main list because it introduces one task-centric attention and
  inverse-dynamics training method evaluated against DreamerV3, not an overview
  or general research framing.
- `WorldClaw: Agentic 3D Open-World Generation at Scale` (`2608.05248`) was not
  placed in the main list because it is an agentic 3D scene-generation system.
  “World” refers primarily to editable open-world content, and the paper does not
  survey or define learned action-conditioned world models.
- `HelloWorld: Enabling Socially Interactive Characters in Video World Models`
  (`2608.05070`) was not placed in the main list because it presents one
  self-distilled interaction-control method and HelloWorldBench. Its project
  artifact is useful for tracking social interaction, but it is not an overview
  work.

- `When Agentic AI Meets Integrated Sensing and Communication` (`2608.05792`)
  was not placed in the main list because it surveys agentic ISAC; predictive
  world models appear only as one open challenge rather than the central subject.
- `Robust-WAM: Bridging Generative Pretraining and Semantic Foresight in
  World-Action Models` (`2608.05903`) was not placed in the main list because it
  proposes one semantic-foresight post-training method rather than an overview or
  field-level framing contribution.
- `JoyAI-RA 0.5: Scaling Robot Manipulation Learning via Dual Action Alignment`
  (`2608.05674`) was not placed in the main list because it presents one VLWA
  architecture and training system, not a survey, taxonomy, roadmap, or definition.
- `HERA: Historical Evidence Routing Adapter for Physical Prediction in Latent
  World Models` (`2608.05523`) was not placed in the main list because it evaluates
  one memory-routing adapter for a frozen predictor rather than an overview work.
- `From Passive Mirrors to Active Agents: Holonic Digital Twins for Physical AI
  over Networks` (`2608.06227`) was not placed in the main list because its primary
  contribution is a specific networked digital-twin architecture; world models
  motivate the problem but are not the overview subject.
- `WorldCycle: Self-Verifiable Reinforcement Learning for Long-Horizon Video World
  Models` (`2608.04964`) was not placed in the main list because it introduces one
  cycle-consistency RL method and benchmark rather than a reusable field taxonomy
  or roadmap.
- `Quantum-Structured World Models (QSWMs) for Predictive Latent Dynamics`
  (`2608.05371`) was not placed in the main list because it proposes and tests one
  quantum-inspired latent architecture rather than surveying or framing the field.
- `Overcoming Statistical Bias in Action-Controllable World Models` (`2608.04653`)
  was not placed in the main list because it introduces the CoCo method and its
  evaluation metrics as a single-method contribution.
- `muSync-GS: Physics-Synchronized Driving Video Synthesis for Weather and
  Geometric Road Hazards` (`2608.04412`) was not placed in the main list because it
  is a specific driving-video synthesis system; generative world models are only
  application context.
- `Faster-WAM: Efficient Inference-Time Future Conditioning for Robust World Action
  Models` (`2608.04404`) was not placed in the main list because it is a specific
  efficient WAM architecture and empirical study, not an overview-style paper.
- `Towards Spatial Supersensing in the Wild` (`2607.13681`) was not placed
  in the main list because its primary contribution is the VSI-Super-Wild
  benchmark and a benchmark-derived failure taxonomy, rather than an overview,
  definition, roadmap, or reusable framework for world-model research.
- `M4World: A Multi-view Multimodal Driving World Model for Interactive Object
  Manipulation and Minute-long Streaming` (`2607.14005`) was not placed in the
  main list because it introduces and evaluates one driving-world generation
  system rather than an overview-style contribution.
- `GigaWorld-Policy-0.5: A Faster and Stronger WAM Empowered by AutoResearch`
  (`2607.13960`) was not placed in the main list because it is an incremental
  action-centered WAM architecture and training study, not a survey, taxonomy,
  definition, roadmap, or field-level framework.
- `Equilibrium Information Aggregation under Machine Learning` (`2607.13670`)
  was not placed in the main list because “world-models” refers to agents'
  heterogeneous beliefs in a theoretical-economics model, not learned world
  models as the research subject.
- `FlowWAM: Optical Flow as a Unified Action Representation for World Action
  Models` (`2607.13017`) was not placed in the main list because it proposes
  one optical-flow action representation and dual-stream diffusion method,
  rather than an overview or general framing contribution.
- `Xiaomi-Robotics-U0: Unified Embodied Synthesis with World Foundation Model`
  (`2607.11643`) was not placed in the main list because it introduces and
  evaluates one 38B embodied-synthesis model rather than an overview,
  taxonomy, definition, roadmap, or field-level framework.
- `WALA Learning Executable Latent Actions from Action-Labeled Demonstrations
  and Action-Free Videos` (`2607.11397`) was not placed in the main list
  because its trainable latent world model is one component of a specific
  robot-policy training method, not the subject of an overview or framing work.
- `Cycle-World: Mitigating Error Accumulation in Long-term Video World Models
  via Reverse-Prediction Cycle Consistency` (`2607.11836`) was not placed in
  the main list because it proposes a single cycle-consistency method for
  long-video generation rather than an overview-style contribution.
- `ABot-3DWorld 0: A Universal World Model to Explore Any 3D Space`
  (`2607.11673`) was not placed in the main list because it presents a specific
  multimodal 3D-generation pipeline and empirical system, not a survey,
  roadmap, taxonomy, definition, or reusable field framework.
- `World Models as Adversaries: Multi-Agent Self-Play Fine-Tuning for Robust
  Motion Planning` (`2607.10630`) was not placed in the main list because it
  develops one adversarial fine-tuning method for autonomous-driving planning.
- `Religion and Artificial Intelligence as Distributed Meaning Systems: A
  Naturalistic Conceptual Model` (`2607.10011`) was not placed in the main list
  because "world-model construction" is used in a distributed-cognition sense;
  learned world models are not the paper's research subject.
- `Causally Debiased Latent Action Model for Embodied Action Conditioned World
  Models` (`2607.09185`) was not placed in the main list because it proposes and
  evaluates one latent-action fine-tuning method rather than an overview,
  taxonomy, definition, roadmap, or broadly reusable field-level framework.
- `GATS: Graph-Augmented Tree Search with Layered World Models for Efficient
  Agent Planning` (`2607.08894`) was not placed in the main list because it is a
  specific tree-search planning method whose layered world model is an internal
  component, not an overview or general framework for world-model research.
- `WCog-VLA: A Dual-Level World-Cognitive Vision-Language-Action Model for
  End-to-End Autonomous Driving` (`2607.08375`) was not placed in the main list
  because it introduces a specific driving architecture and dataset rather than
  an overview, taxonomy, position, definition, or broadly reusable framework.
- `AI Agent Systems: Architectures, Applications, and Evaluation` was not placed in
  the main list because it treats world models as one component in a broader agent
  taxonomy.
- `Critique of Agent Model` was not placed in the main list because its main subject
  is agent-model critique; world models appear as one architectural component.
- `Dual-Channel Grounded World Modeling (DCGWM)` was not placed in the main list
  because it is a problem-formulation/architecture manuscript rather than a survey,
  review, roadmap, or taxonomy paper.
- General Wikipedia pages were used only as orientation during search, not as canonical
  metadata sources.

## Next Search Ideas

- Search by new arXiv IDs after `2607`.
- Check conference proceedings and journal pages for accepted versions of arXiv preprints.
- Track new repositories named `awesome-world-model`, `world-model-survey`,
  `interactive-world-model`, and `medical-world-model`.
