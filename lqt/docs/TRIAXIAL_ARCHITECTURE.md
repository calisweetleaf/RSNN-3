# LQT/LQF Triaxial Architecture — Domain Model and Substrate Integration

**Classification:** INTERNAL
**Version:** 1.0
**Date:** 2026-09-21
**Origin:** Authority-intake documentation pass (packet LQT-001 follow-on)
**Status:** OPERATIONAL REFERENCE

---

## 1. Executive Summary

The LQT system is one axis of a three-axis domain model in which recursive
tensors carry structure and evolution, ethical tensors carry purpose and
alignment, and metacognitive tensors carry awareness and self-modeling. This
document specifies the domain model as it actually exists in this repository:
the RTA/RWA/LQT boundary contract, the operator's Python reference
implementations of the ethical and metacognitive axes, and the
autodidactic-learning-substrate train-cycle that binds them. It also records
the duplication ruling for `iala/`. Authority precedence follows
`docs/AUTHORITY_COMPLIANCE_MATRIX.md`; where this document states a boundary,
it cites the whitepaper clause or the substrate README that fixes it.

## 2. The Three Axes

### 2.1 Domain model

The triaxial whitepaper (§2.1) defines the manifold Ψ = ⟨T_R, T_E, T_M⟩.
The load-bearing reading for this repository is not the consciousness theory
— it is the *separation of concerns* the three axes force:

| Axis | Tensor | Responsibility | Carried in this repo by |
|---|---|---|---|
| Structure | Recursive Tensor (T_R) | Structural evolution, self-referential patterns, structural attention over knowledge entities | `include/lqt/rta.h`, `rta_ops.h`, `rta_analysis.h` (structure + operations); `RTAAttention` in `autodidactic-learning-substrate/autodidactic_learning.py:936` (selection role) |
| Purpose | Ethical Tensor (T_E) | Five-dimension value alignment, dialectical synthesis, breath-phase modulation of behavior | `original-py-code/ethical_tensor.py` (reference implementation); `EthicalLearningFilter` in the substrate (lines 218–341). No C++ surface |
| Awareness | Metacognitive Tensor (T_M) | 15-component self-model, contradiction depth, identity coherence, loop interception | `original-py-code/metacognitive_tensor.py` (reference implementation); `MetacognitiveMonitor` in the substrate (lines 499–556). No C++ surface |

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 560" font-family="Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#10141f"/>
      <stop offset="100%" stop-color="#1c2438"/>
    </linearGradient>
    <linearGradient id="rGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2e7d6b"/>
      <stop offset="100%" stop-color="#54c9a8"/>
    </linearGradient>
    <linearGradient id="eGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8a4a2e"/>
      <stop offset="100%" stop-color="#e0a35c"/>
    </linearGradient>
    <linearGradient id="mGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#3b4f8a"/>
      <stop offset="100%" stop-color="#7fa8e8"/>
    </linearGradient>
    <radialGradient id="coreGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#f2f5ff"/>
      <stop offset="70%" stop-color="#b9c6e8"/>
      <stop offset="100%" stop-color="#7d8bb5"/>
    </radialGradient>
    <filter id="softBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="7"/>
    </filter>
    <filter id="haloBlur" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="14"/>
    </filter>
  </defs>

  <rect width="920" height="560" fill="url(#bgGrad)"/>
  <text x="460" y="42" fill="#dfe6f5" font-size="20" text-anchor="middle" letter-spacing="2">TRIAXIAL DOMAIN MODEL — AXES, ROLES, SUBSTRATES</text>

  <!-- glow halos -->
  <circle cx="270" cy="170" r="105" fill="url(#rGrad)" opacity="0.18" filter="url(#haloBlur)"/>
  <circle cx="650" cy="170" r="105" fill="url(#eGrad)" opacity="0.18" filter="url(#haloBlur)"/>
  <circle cx="460" cy="400" r="105" fill="url(#mGrad)" opacity="0.18" filter="url(#haloBlur)"/>

  <!-- axis triangles -->
  <polygon points="270,170 650,170 460,400" fill="none" stroke="#5a6a93" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.8"/>

  <!-- T_R node -->
  <circle cx="270" cy="170" r="86" fill="url(#rGrad)" filter="url(#softBlur)" opacity="0.35"/>
  <circle cx="270" cy="170" r="78" fill="#152018" stroke="#54c9a8" stroke-width="2"/>
  <text x="270" y="140" fill="#8fe6c9" font-size="15" text-anchor="middle" font-weight="bold">T_R — RECURSIVE TENSOR</text>
  <text x="270" y="162" fill="#c9e8dc" font-size="11" text-anchor="middle">structure / evolution</text>
  <text x="270" y="180" fill="#c9e8dc" font-size="11" text-anchor="middle">self-referential patterns</text>
  <text x="270" y="198" fill="#c9e8dc" font-size="11" text-anchor="middle">structural attention (RTA)</text>
  <text x="270" y="222" fill="#7ba794" font-size="10" text-anchor="middle">rta.h · rta_ops.h · rta_analysis.h</text>

  <!-- T_E node -->
  <circle cx="650" cy="170" r="86" fill="url(#eGrad)" filter="url(#softBlur)" opacity="0.35"/>
  <circle cx="650" cy="170" r="78" fill="#1f1712" stroke="#e0a35c" stroke-width="2"/>
  <text x="650" y="140" fill="#f0c993" font-size="15" text-anchor="middle" font-weight="bold">T_E — ETHICAL TENSOR</text>
  <text x="650" y="162" fill="#efe0c8" font-size="11" text-anchor="middle">purpose / alignment</text>
  <text x="650" y="180" fill="#efe0c8" font-size="11" text-anchor="middle">5 ethical dimensions</text>
  <text x="650" y="198" fill="#efe0c8" font-size="11" text-anchor="middle">breath-phase modulation</text>
  <text x="650" y="222" fill="#a58f6e" font-size="10" text-anchor="middle">ethical_tensor.py (reference only)</text>

  <!-- T_M node -->
  <circle cx="460" cy="400" r="86" fill="url(#mGrad)" filter="url(#softBlur)" opacity="0.35"/>
  <circle cx="460" cy="400" r="78" fill="#131722" stroke="#7fa8e8" stroke-width="2"/>
  <text x="460" y="370" fill="#a9c6f2" font-size="15" text-anchor="middle" font-weight="bold">T_M — METACOGNITIVE TENSOR</text>
  <text x="460" y="392" fill="#d5e2f7" font-size="11" text-anchor="middle">awareness / self-modeling</text>
  <text x="460" y="410" fill="#d5e2f7" font-size="11" text-anchor="middle">15-component state M</text>
  <text x="460" y="428" fill="#d5e2f7" font-size="11" text-anchor="middle">contradiction · identity · loops</text>
  <text x="460" y="452" fill="#7a8aa8" font-size="10" text-anchor="middle">metacognitive_tensor.py (reference only)</text>

  <!-- center manifold -->
  <circle cx="460" cy="255" r="46" fill="url(#coreGrad)" filter="url(#softBlur)" opacity="0.9"/>
  <circle cx="460" cy="255" r="30" fill="#e8edf8" stroke="#ffffff" stroke-width="1.5"/>
  <text x="460" y="250" fill="#1a2233" font-size="11" text-anchor="middle" font-weight="bold">Ψ =</text>
  <text x="460" y="266" fill="#1a2233" font-size="11" text-anchor="middle">⟨T_R, T_E, T_M⟩</text>

  <!-- axis labels on edges -->
  <text x="460" y="152" fill="#8fa0c4" font-size="10" text-anchor="middle">entanglement (REP, triaxial §2.4)</text>
  <text x="345" y="300" fill="#8fa0c4" font-size="10" text-anchor="middle">coherence pressure</text>
  <text x="585" y="300" fill="#8fa0c4" font-size="10" text-anchor="middle">paradox signals</text>

  <!-- footer note -->
  <text x="460" y="530" fill="#6f7c99" font-size="10.5" text-anchor="middle">Only T_R has a C++ surface in this repository. T_E and T_M exist as the operator's Python reference and the substrate adapters.</text>
</svg>

*Figure 1 — Triaxial domain model. Glow edges mark the interaction surfaces;
dashed triangle marks the integration operator Ψ (triaxial paper §3.8),
which is asserted by theory and not implemented in either tree (matrix row G1).*

### 2.2 Recursive Tensor axis (T_R)

Semantics per the RTA whitepaper §2.2, as realized in `include/lqt/rta.h`
DD-02: five dimensions d0 Feature / d1 Pattern / d2 Temporal / d3 Scale /
d4 Channel. The structural half of the axis is the wire-format block
(`RtaBlock`, CRC-64 protected, six sparse encodings) plus the operations
layer (`rta_ops.h` contract/project/expand; `rta_analysis.h` fractal
iteration, entropy, normalization, density). What this axis does **not** yet
do, per matrix rows E7/E15: reference resolution and value reconstruction.
Treat RTA as structure-and-operations, not as a completed self-referential
value system.

### 2.3 Ethical Tensor axis (T_E)

The reference implementation `original-py-code/ethical_tensor.py` fixes five
normative dimensions (line 17):

```
# ethical_tensor.py — ETHICAL_DIMENSIONS
["good_harm", "truth_deception", "fairness_bias", "liberty_constraint", "care_harm"]
```

Behavioral mechanics that define the axis:

- **BreathPhase modulation** — four phases (INHALE, HOLD_IN, EXHALE,
  HOLD_OUT; line 24) with phase-dependent coherence factors (1.2 / 1.5 /
  0.8 / 0.5), collapse thresholds (0.9 / 0.95 / 0.6 / 0.7), and vacuum
  fluctuation scales (`QuantumBreathAdapter`, lines 123–197). Inhale scales
  the ethical tensor by `1.0 + 0.5·progress`; exhale by
  `1.0 − 0.3·progress`; hold phases pass through unmodulated.
- **NarrativeArchetype field modulations** — each archetype carries an
  ethical vector, a quantum signature, influence radius, and intensity; its
  field modulation is composed from a base band (0.95–1.05), a per-axis
  sinusoidal signature term, and archetype-specific patterns: Creation
  (randomized-center Gaussian), Destruction (randomized-frequency
  interference), Rebirth (spiral `sin(r + 5θ)`), Transcendence (rising
  gradients), Equilibrium (harmonic cosines) — all clipped to [0.1, 2.0]
  (`to_field_modulation`, lines 44–117).
- **Collapse interpretation** — `CollapseAdapter.interpret_collapse`
  (lines 625–710) locates the maximum density change, computes magnitude
  and entropy delta, samples the ethical vector at the collapse site,
  matches it to the strongest archetype above 0.7 similarity, and produces
  a breath-phase-dependent narrative reading.
- **Ethical force coupling** — `apply_ethical_force` (lines 2062–2087)
  modulates a field state by `coupling · Σ_d ethical_field_d` and
  renormalizes; `analyze_ethical_distribution` (lines 2089–2115) reports
  per-dimension statistics.

The whitepaper grounding is triaxial §2.3 (Ethical Tensor Dynamics, the ERE
recursion with coherence stiffness β_t) and §2.6 (BVT-2). The Python
reference implements the *static field* semantics above; the
eigenrecursive update loop of §2.3 lives in the metacognitive engine's
`EigenrecursiveBayesianCore` (see §2.4) rather than in `ethical_tensor.py`.

### 2.4 Metacognitive Tensor axis (T_M)

`original-py-code/metacognitive_tensor.py` implements the axis in two tiers.
The state vector is the 15-component `MetacognitiveState`
(lines 22–42): confidence, uncertainty, justification, coherence, boundary
awareness, resource allocation, strategy selection, temporal dynamics, error
detection, learning rate, self-representation, narrative continuity, goal
alignment, counterfactual simulation, introspective resolution — matching
metacognitive paper §2.1 component-for-component.

Five component engines (paper §3.1.1–§3.1.5, all present in Python):

| Engine | Lines | Core mechanism |
|---|---|---|
| ContradictionDepthField | 44–111 | Paradox potential Π = boundary integral of value gradient over the ethical manifold + 0.7·temporal variance of the contradiction history; BVT-2 contradiction detection via cosine/negation similarity with 0.7 resolution threshold |
| CoherenceTraceMap | 113–201 | Information-flow matrix with 0.9/0.1 exponential smoothing; loop stability via Jacobian-approximation eigenvalues (stability = 1 − max|λ|) over a 10-state window |
| ReflectiveIndexLayer | 203–264 | Per-layer awareness = mean(self-reference, activation entropy, meta-capacity); metacognitive depth = weighted sum with layer weights [1, 2, 3] |
| FeedbackEntropyVector | 266–331 | Shannon entropy per cycle; cycle-to-cycle KL as mutual-information proxy; stability = 1/(1 + entropy variance) |
| IdentityCoherenceTensor | 333–432 | Slow core-identity adaptation (0.95/0.05); coherence = 0.6·core + 0.4·temporal; drift metrics over the identity trace |

Three integration engines (paper §3.2, in `AdvancedMetacognitiveTensor`):

| Engine | Lines | Core mechanism |
|---|---|---|
| TemporalEigenstateEngine | 720–826 | t_i(d) = t_e·∏δ_j with depth-compressed dilation `1/(1 + 0.1·d)`; causal-inversion paradox detection; regime classification (compression < 0.5, equilibrium, expansion > 1.5) |
| RecursiveLoopInterceptor | 828–1016 | RLDIS v1.1: pattern signature (sequential cosine similarity + state-norm influence), contradiction-spiral detection (sim(i, i−2) > 0.8 while sim(i, i−1) < 0.3), self-reference density via half-vector autocorrelation, resource-anomaly detection (norm > 2σ of trailing window); six-pattern taxonomy with severity 1–3 |
| EigenrecursiveBayesianCore | 1018–1192 | RBUS posterior from softmax likelihood·prior; ethical projection π_ℰ via softmax-weighted manifold; belief update `B_t = posterior · exp(−β_t·KL)`; prior loop closure at 0.9/0.1; adaptive β_t bounded [0.01, 2.0]; volitional activity V* = ethical momentum / belief norm |

Consciousness gating: the base `MetacognitiveTensor.forward` (lines
474–570) folds the five component outputs into a five-input sigmoid gate;
`consciousness_threshold` default 0.8. This is a Python `nn.Module` with
learned `nn.Linear` layers — a py→cpp conversion must decide whether those
layers are serialized artifacts (weights must then be carried) or replaced
by the fixed mathematical core (the gate reduces to a logistic function of
five normalized scalars; see the conversion contract, §5 of
`docs/PY_TO_CPP_CONVERSION_CONTRACT.md`).

## 3. Weight Storage: "Buckets of Knowledge"

The storage doctrine, fixed by the substrate README boundary section and
consistent with triaxial §2.2–§2.3:

> RTA is structural attention: it selects which knowledge entities receive
> computation. RWA is recursive weight/state storage: it carries
> representations, recursive references, phase/error state, and evolution
> history. LQT remains the parameter/value container and C++ runtime
> boundary.

Read concretely: **weights live in LQT containers; tensors compute them.**

- The **quantized parameter payload** — codebooks, indices, deltas, sparse
  masks — is an LQT container concern (§5-A of the compliance matrix).
- The **recursive weight quintuple {B, Φ, R, T, ε}** is the RWA unit of
  stored state: a base codebook index, a phase-modulation vector, a
  reference matrix stack, a 5-float RTA positional embedding, and an error
  preservation vector (`include/lqt/recursive_weight.h:83-104`). Its
  effective value is computed, not stored:
  `W_eff(i,t) = B + α·W_eff(i−1,t) + Σ R_j·W_ref(j,t) + Φ(t) + ε`
  (`include/lqt/rw_compute.h`, Theorem 1.2.1 fixed point
  `W_∞ = (B + R_contrib + Φ + ε)/(1 − α)` for |α| < 1).
- In the substrate, each knowledge "bucket" is a `TriaxialKnowledgeEntity`
  (`autodidactic_learning.py:748–800`) holding content, ethical vector,
  abstraction level, and a `LocalRWAWeight` (lines 342–368) that mirrors the
  quintuple contract in torch form with evolution and ethical guidance.

The honest current state, stated so no reader over-trusts it: no code path
today serializes a trained substrate weight into an `.lqt` container, and
the native `.rw` persistence contract is unimplemented on both sides (matrix
row F6, substrate README remaining-work item 2). The bucket doctrine is an
architectural contract with one exercised C++ side (RW structures, tests)
and one registry-fallback Python side.

## 4. The Autodidactic Learning Substrate

### 4.1 Position in the system

`autodidactic-learning-substrate/` is the parameter source: the train loop
that decides which knowledge enters RWA state, how it evolves, and when it
is gated. Its README fixes the stage contract:

```
# autodidactic-learning-substrate/README.md — Current train-cycle contract
RTA attention -> RWA recursive state -> RAL transform -> RBUS update
  -> URSMIF monitor -> RAL-RSRE stability gate -> RLA checkpoint
```

Stage authorities (README theorem-routing table): RAL moves between
abstraction levels with coherence checks; RBUS updates bounded
evidence/posterior state; URSMIF detects contradiction and recursive
instability; the RAL–RSRE bridge applies intervention and stability gates;
RLA runs bounded cycles and checkpoints; RLM stays an experience-driven
adapter for goal/value formation. The seven source papers under `theorems/`
are loaded as authority metadata with an explicit disclaimer that their full
proofs are not implemented.

### 4.2 Cycle mechanics as executed

`run_training_cycle()` (`autodidactic_learning.py:1379–1414`) is the
executable form of the contract. One cycle:

1. Select a breath phase (externally supplied, or round-robin over the
   substrate's breath taxonomy).
2. Dispatch phase behavior: INHALE → acquisition burst; HOLD-family →
   integration; EXHALE → synthesis burst; REST-family → consolidation;
   DREAM → dream-learning cycle.
3. Update the metacognitive state.
4. On the configured cadence, run the stability monitor and apply
   intervention if unstable (the URSMIF/RAL-RSRE gate).
5. Update performance metrics and validate the cycle against the theorem
   contract (`CoreTheoremSubstrate.validate_cycle`, lines 109–120, checked
   against `cycle_contract()` — the seven-stage ordering above).
6. Increment the cycle counter and return the telemetry dict.

The content boundary is a deterministic, parameter-free encoder
(`DeterministicContentEncoder`, lines 129+), installed specifically to
replace silent random-vector injection; the README names a real
embedding provider as remaining work item 1.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 620" font-family="Helvetica, Arial, sans-serif">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e1219"/>
      <stop offset="100%" stop-color="#1a2130"/>
    </linearGradient>
    <linearGradient id="stageGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#3d5a80"/>
      <stop offset="100%" stop-color="#22354e"/>
    </linearGradient>
    <linearGradient id="gateGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7a3b3b"/>
      <stop offset="100%" stop-color="#4a2222"/>
    </linearGradient>
    <linearGradient id="okGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2e7d6b"/>
      <stop offset="100%" stop-color="#1a4a3e"/>
    </linearGradient>
    <filter id="blur2" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="5"/>
    </filter>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#9db2d9"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#e08a8a"/>
    </marker>
  </defs>

  <rect width="960" height="620" fill="url(#bg2)"/>
  <text x="480" y="40" fill="#dfe6f5" font-size="19" text-anchor="middle" letter-spacing="2">AUTODIDACTIC TRAIN CYCLE — STAGE CONTRACT AND FEEDBACK PATHS</text>
  <text x="480" y="60" fill="#77859f" font-size="11" text-anchor="middle">autodidactic_learning.py run_training_cycle() · stage order fixed by cycle_contract()</text>

  <!-- stage row -->
  <g font-size="11" text-anchor="middle">
    <rect x="30"  y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#5f7ca8" filter="url(#blur2)" opacity="0.5"/>
    <rect x="30"  y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#7fa2d0" stroke-width="1.5"/>
    <text x="90"  y="148" fill="#cfe0f5" font-weight="bold">1 · RTA</text>
    <text x="90"  y="166" fill="#a9bedd" font-size="10">attention</text>
    <text x="90"  y="180" fill="#7a8fae" font-size="9">select entities</text>

    <rect x="170" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#5f7ca8" filter="url(#blur2)" opacity="0.5"/>
    <rect x="170" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#7fa2d0" stroke-width="1.5"/>
    <text x="230" y="148" fill="#cfe0f5" font-weight="bold">2 · RWA</text>
    <text x="230" y="166" fill="#a9bedd" font-size="10">recursive state</text>
    <text x="230" y="180" fill="#7a8fae" font-size="9">store / evolve weights</text>

    <rect x="310" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#5f7ca8" filter="url(#blur2)" opacity="0.5"/>
    <rect x="310" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#7fa2d0" stroke-width="1.5"/>
    <text x="370" y="148" fill="#cfe0f5" font-weight="bold">3 · RAL</text>
    <text x="370" y="166" fill="#a9bedd" font-size="10">transform</text>
    <text x="370" y="180" fill="#7a8fae" font-size="9">abstraction ladder</text>

    <rect x="450" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#5f7ca8" filter="url(#blur2)" opacity="0.5"/>
    <rect x="450" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#7fa2d0" stroke-width="1.5"/>
    <text x="510" y="148" fill="#cfe0f5" font-weight="bold">4 · RBUS</text>
    <text x="510" y="166" fill="#a9bedd" font-size="10">update</text>
    <text x="510" y="180" fill="#7a8fae" font-size="9">bounded posterior</text>

    <rect x="590" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#5f7ca8" filter="url(#blur2)" opacity="0.5"/>
    <rect x="590" y="120" width="120" height="74" rx="9" fill="url(#stageGrad)" stroke="#7fa2d0" stroke-width="1.5"/>
    <text x="650" y="148" fill="#cfe0f5" font-weight="bold">5 · URSMIF</text>
    <text x="650" y="166" fill="#a9bedd" font-size="10">monitor</text>
    <text x="650" y="180" fill="#7a8fae" font-size="9">contradiction / instability</text>

    <rect x="730" y="120" width="100" height="74" rx="9" fill="url(#gateGrad)" stroke="#b06a6a" filter="url(#blur2)" opacity="0.5"/>
    <rect x="730" y="120" width="100" height="74" rx="9" fill="url(#gateGrad)" stroke="#c98a8a" stroke-width="1.5"/>
    <text x="780" y="148" fill="#f0cfcf" font-weight="bold">6 · RAL–RSRE</text>
    <text x="780" y="166" fill="#e0b8b8" font-size="10">stability gate</text>
    <text x="780" y="180" fill="#a97e7e" font-size="9">intervene if unstable</text>

    <rect x="850" y="120" width="90" height="74" rx="9" fill="url(#okGrad)" stroke="#5fb89c" filter="url(#blur2)" opacity="0.5"/>
    <rect x="850" y="120" width="90" height="74" rx="9" fill="url(#okGrad)" stroke="#7fd6b4" stroke-width="1.5"/>
    <text x="895" y="148" fill="#cfeee0" font-weight="bold">7 · RLA</text>
    <text x="895" y="166" fill="#b0dcc8" font-size="10">checkpoint</text>
    <text x="895" y="180" fill="#7aa890" font-size="9">bounded cycle</text>
  </g>

  <!-- forward arrows -->
  <g stroke="#9db2d9" stroke-width="1.6">
    <line x1="150" y1="157" x2="166" y2="157" marker-end="url(#arrow)"/>
    <line x1="290" y1="157" x2="306" y2="157" marker-end="url(#arrow)"/>
    <line x1="430" y1="157" x2="446" y2="157" marker-end="url(#arrow)"/>
    <line x1="570" y1="157" x2="586" y2="157" marker-end="url(#arrow)"/>
    <line x1="710" y1="157" x2="726" y2="157" marker-end="url(#arrow)"/>
    <line x1="830" y1="157" x2="846" y2="157" marker-end="url(#arrow)"/>
  </g>

  <!-- intervention loop back -->
  <path d="M 780 198 L 780 250 L 370 250 L 370 200" fill="none" stroke="#e08a8a" stroke-width="1.6" stroke-dasharray="6 4" marker-end="url(#arrowRed)"/>
  <text x="575" y="242" fill="#e0a0a0" font-size="10" text-anchor="middle">intervention path: gate failure re-enters at RAL transform</text>

  <!-- validation loop -->
  <path d="M 895 198 L 895 300 L 90 300 L 90 198" fill="none" stroke="#8fd6b4" stroke-width="1.4" stroke-dasharray="4 4" marker-end="url(#arrow)"/>
  <text x="490" y="292" fill="#8fd6b4" font-size="10" text-anchor="middle">theorem-contract validation (CoreTheoremSubstrate.validate_cycle) closes the cycle</text>

  <!-- substrate inputs -->
  <g font-size="10.5">
    <rect x="60" y="370" width="250" height="88" rx="9" fill="#1b2436" stroke="#5f7ca8" stroke-width="1.2"/>
    <text x="185" y="394" fill="#cfe0f5" text-anchor="middle" font-weight="bold">Knowledge graph</text>
    <text x="185" y="412" fill="#8fa3c4" text-anchor="middle" font-size="9.5">TriaxialKnowledgeEntity buckets (748–800)</text>
    <text x="185" y="428" fill="#8fa3c4" text-anchor="middle" font-size="9.5">EnhancedKnowledgeGraph relationships (805+)</text>
    <text x="185" y="444" fill="#8fa3c4" text-anchor="middle" font-size="9.5">RTAAttention.select (936–952)</text>

    <rect x="355" y="370" width="250" height="88" rx="9" fill="#1b2436" stroke="#e0a35c" stroke-width="1.2"/>
    <text x="480" y="394" fill="#f0d9b5" text-anchor="middle" font-weight="bold">Ethical filter</text>
    <text x="480" y="412" fill="#c4a97f" text-anchor="middle" font-size="9.5">EthicalLearningFilter (218–341)</text>
    <text x="480" y="428" fill="#c4a97f" text-anchor="middle" font-size="9.5">5-dimension vectors gate acquisition</text>
    <text x="480" y="444" fill="#c4a97f" text-anchor="middle" font-size="9.5">breath-phase-aware modulation</text>

    <rect x="650" y="370" width="250" height="88" rx="9" fill="#1b2436" stroke="#7fa8e8" stroke-width="1.2"/>
    <text x="775" y="394" fill="#c4d7f5" text-anchor="middle" font-weight="bold">Metacognitive monitor</text>
    <text x="775" y="412" fill="#8fa3c4" text-anchor="middle" font-size="9.5">MetacognitiveMonitor (499–556)</text>
    <text x="775" y="428" fill="#8fa3c4" text-anchor="middle" font-size="9.5">ContradictionDetector · IdentityCoherenceTracker</text>
    <text x="775" y="444" fill="#8fa3c4" text-anchor="middle" font-size="9.5">feeds stage 5</text>
  </g>

  <g stroke="#5a6a93" stroke-width="1.3">
    <line x1="185" y1="366" x2="185" y2="330"/>
    <line x1="480" y1="366" x2="480" y2="330"/>
    <line x1="775" y1="366" x2="775" y2="330"/>
  </g>
  <text x="480" y="322" fill="#77859f" font-size="10" text-anchor="middle">substrate inputs enter the cycle at attention, monitoring, and acquisition filtering</text>

  <!-- bottom boundary note -->
  <rect x="60" y="500" width="840" height="76" rx="9" fill="#141a28" stroke="#3d4a66" stroke-width="1.2"/>
  <text x="480" y="526" fill="#aebcd8" font-size="11" text-anchor="middle" font-weight="bold">LQT/RWA boundary</text>
  <text x="480" y="545" fill="#77859f" font-size="10" text-anchor="middle">weights live in LQT containers; tensors compute them. Current reality: RWA state persists in a Python registry only —</text>
  <text x="480" y="561" fill="#77859f" font-size="10" text-anchor="middle">the native .rw serializer/loader contract and the LQT-container write-back path are both unimplemented (matrix row F6).</text>
</svg>

*Figure 2 — The autodidactic train cycle. Solid arrows are the forward
stage contract; the red dashed path is the RAL–RSRE intervention loop; the
green dashed path is theorem-contract validation closing each cycle.*

## 5. Breath-Phase Taxonomy Conflict

Two incompatible breath taxonomies coexist in the archive and any conversion
or integration work must surface this before writing code:

- `original-py-code/ethical_tensor.py:24–29`: **INHALE, HOLD_IN, EXHALE,
  HOLD_OUT** (4 phases), with the coherence/collapse/vacuum parameter
  tables of §2.3.
- `autodidactic-learning-substrate/autodidactic_learning.py:171–191`:
  imports `sacred_harmonic_ratio.BreathPhase` (7-phase system with PHI/TAU
  sacred-ratio synchronizer) and, when that import fails, falls back to a
  local **INHALE, PAUSE_RISING, HOLD, EXHALE, PAUSE_FALLING, REST, DREAM**
  enum. The substrate degrades to `BREATH_SYSTEM_AVAILABLE = False` and
  loses phase routing when its import is missing.

The two enums share only INHALE and EXHALE by name. The C++ conversion
contract (`docs/PY_TO_CPP_CONVERSION_CONTRACT.md`) carries this as an open
ruling for the operator.

## 6. Integration Status of the Three Axes in C++

Stated without optimism padding:

- **T_R** is the only axis with a C++ surface. Its structure layer is
  tested (matrix rows E3, E4, E12–E14); its value layer is not (E7, E15).
- **T_E** and **T_M** have zero C++ surface. The reference implementations
  are the operator's Python files; the substrate carries simplified
  adapters (EthicalLearningFilter, MetacognitiveMonitor,
  ContradictionDetector, IdentityCoherenceTracker) that reuse the
  vocabulary but not the full engine math (no TemporalEigenstateEngine, no
  RecursiveLoopInterceptor taxonomy, no full RBUS in the substrate's
  monitors).
- The **Ψ integration operator** of triaxial §3.8
  (`tanh(W_R·T_R + W_E·T_E + W_M·T_M)`) is implemented nowhere.
  `metacognitive_tensor.py:1367 compute_triaxial_integration_score` is a
  weighted-average heuristic, not the specified operator.

## 7. Directory Duplication Ruling: `iala/` vs `autodidactic-learning-substrate/`

I verified the duplication directly rather than trusting directory names:

```
$ md5sum autodidactic-learning-substrate/autodidactic_learning.py iala/autodidactic_learning.py
1b6aadeaf983f63299d69a47a6cc92e4  autodidactic-learning-substrate/autodidactic_learning.py
1b6aadeaf983f63299d69a47a6cc92e4  iala/autodidactic_learning.py
$ diff -rq autodidactic-learning-substrate iala
Only in autodidactic-learning-substrate: autodidactic_substrate
```

Ruling: `iala/` is a byte-identical twin of
`autodidactic-learning-substrate/` for both Python files, the static test,
the README, and all seven theorem papers. The only delta is an empty
`autodidactic_substrate/` directory present in the newer copy. The file
header of `autodidactic_learning.py` self-identifies as "Integrated
Autodidactic Learning Architecture (IALA) … For Project rené", which
explains the twin's name. Consequences:

1. Read the substrate from either path today; results are identical.
2. Do not edit one twin and expect the other to follow — there is no link
   between them, and divergence will be silent.
3. The duplication itself is undocumented in `filetree.md`, which lists
   `iala/` only. Flagging it here so the next agent does not treat `iala/`
   as a distinct subsystem or cite both as independent evidence.

The disposition (delete, symlink, or promote one to canonical) is an
operator ruling I am not authorized to make; recorded as an open item.

## 8. Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-09-21 | Initial triaxial domain model: axes, weight-storage doctrine, substrate cycle, breath-taxonomy conflict, iala duplication ruling. |
