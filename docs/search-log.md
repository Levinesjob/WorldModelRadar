# Search Log

Last checked: 2026-08-11

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
