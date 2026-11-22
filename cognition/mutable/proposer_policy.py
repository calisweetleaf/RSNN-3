"""Proposal heuristics of the self-modification loop (meta-level mutable surface).

runtime/selfmod/proposer.py (protected) reads the engine-state signals of the current
incumbent (objective.score_seed: meta_reflective_head confidence, sentinel severity,
Bayesian concentration/error, motivation drive, IALA learning, |dW|), scores every rule
below with ``rule_score`` and turns the chosen rule into an AST edit of an object-level
module in cognition/mutable. Every constant and function here is itself eligible for
edits by the loop (meta-level, depth 1), accepted only through the same gate.

Rule fields: name, signal, cmp ('>' or '<'), thr (constant name), module, target,
kind ('const_scale' | 'const_add' | 'swap_call' | 'insert_term' | 'reorder'),
step (constant name: factor for const_scale, delta/coef for const_add/insert_term),
weight (constant name), plus kind-specific fields.
"""

# ---------------------------------------------------------------- thresholds
THR_BAYES_CONC_HIGH = 2.0      # log10(alpha+beta): beliefs harder than ~100 pseudo-counts
THR_BAYES_CONC_LOW = 1.0
THR_BAYES_ABS_ERR = 0.01       # mean |evidence - belief mean| on held-out steps
THR_DW_LOW = 1e-4              # mean |dW| per step: plasticity effectively collapsed
THR_DW_HIGH = 0.05
THR_SEVERITY = 0.2
THR_DRIVE_STD = 0.01           # motivation drive barely varies
THR_ADVANTAGE = 0.005          # learning advantage too small to move weights
THR_META_CONF = 0.5            # meta_reflective_head confidence low
THR_REFLECTION_ERRORS = 1.5    # reflection errors per step

# ---------------------------------------------------------------- steps
STEP_BAYES_DECAY = 0.3
STEP_BAYES_SCALE = 0.5
STEP_BAYES_SCALE_UP = 1.5
STEP_FORGETTING = 0.9
STEP_ETA_UP = 3.0
STEP_ETA_DOWN = 0.5
STEP_SEVERITY_GATE = 0.8
STEP_VALENCE_GAIN = 2.0
STEP_W_META = 0.1
STEP_W_NOVELTY = 0.1
STEP_QUALITY_THRESHOLD = 0.9

# ---------------------------------------------------------------- rule weights
W_RULE_BAYES_DECAY = 0.5
W_RULE_BAYES_SCALE = 0.8
W_RULE_BAYES_SCALE_UP = 0.8
W_RULE_FORGETTING = 0.6
W_RULE_ETA_UP = 1.0
W_RULE_ETA_DOWN = 1.0
W_RULE_SEVERITY = 0.7
W_RULE_VALENCE = 0.7
W_RULE_META = 0.5
W_RULE_SWAP_OUTER = 0.5
W_RULE_NOVELTY_TERM = 0.4
W_RULE_QUALITY_THR = 0.3
W_RULE_REORDER = 0.1

# ---------------------------------------------------------------- selection
URGENCY_CAP = 5.0
TABU_PENALTY = 0.5             # per consecutive reject of the same rule
EXPLORATION = 0.15             # probability of picking a random triggered rule
STEP_JITTER = 0.3              # step exponent jitter: factor ** (1 + U(-j, j))
FALLBACK_SIGMA = 0.3           # untriggered fallback: log-normal jitter of one constant
META_TRIGGER_REJECTS = 2       # consecutive rejects of a rule before a meta edit
META_SOFTEN = 0.5              # meta: step -> step ** META_SOFTEN (toward no-op)
META_THR_FACTOR = 1.5          # meta: move the threshold away from the current signal
META_WEIGHT_FACTOR = 0.5       # meta: down-weight the rule

RULES = [
    {"name": "bayes_overconfident_decay", "signal": "bayes_log10_concentration", "cmp": ">",
     "thr": "THR_BAYES_CONC_HIGH", "module": "bayes_policy", "target": "DEPTH_DECAY",
     "kind": "const_scale", "step": "STEP_BAYES_DECAY", "weight": "W_RULE_BAYES_DECAY"},
    {"name": "bayes_overconfident_scale", "signal": "bayes_log10_concentration", "cmp": ">",
     "thr": "THR_BAYES_CONC_HIGH", "module": "bayes_policy", "target": "PSEUDO_COUNT_SCALE",
     "kind": "const_scale", "step": "STEP_BAYES_SCALE", "weight": "W_RULE_BAYES_SCALE"},
    {"name": "bayes_underconfident_scale", "signal": "bayes_log10_concentration", "cmp": "<",
     "thr": "THR_BAYES_CONC_LOW", "module": "bayes_policy", "target": "PSEUDO_COUNT_SCALE",
     "kind": "const_scale", "step": "STEP_BAYES_SCALE_UP", "weight": "W_RULE_BAYES_SCALE_UP"},
    {"name": "bayes_tracking_forgetting", "signal": "bayes_abs_err", "cmp": ">",
     "thr": "THR_BAYES_ABS_ERR", "module": "bayes_policy", "target": "FORGETTING",
     "kind": "const_scale", "step": "STEP_FORGETTING", "weight": "W_RULE_FORGETTING"},
    {"name": "plasticity_collapsed_eta", "signal": "dw_mean", "cmp": "<",
     "thr": "THR_DW_LOW", "module": "plasticity_policy", "target": "ETA",
     "kind": "const_scale", "step": "STEP_ETA_UP", "weight": "W_RULE_ETA_UP"},
    {"name": "plasticity_exploding_eta", "signal": "dw_mean", "cmp": ">",
     "thr": "THR_DW_HIGH", "module": "plasticity_policy", "target": "ETA",
     "kind": "const_scale", "step": "STEP_ETA_DOWN", "weight": "W_RULE_ETA_DOWN"},
    {"name": "sentinel_severity_gate", "signal": "severity_mean", "cmp": ">",
     "thr": "THR_SEVERITY", "module": "plasticity_policy", "target": "SEVERITY_GATE",
     "kind": "const_scale", "step": "STEP_SEVERITY_GATE", "weight": "W_RULE_SEVERITY"},
    {"name": "motivation_flat_drive", "signal": "drive_std", "cmp": "<",
     "thr": "THR_DRIVE_STD", "module": "motivation_policy", "target": "LOOP_VALENCE_GAIN",
     "kind": "const_scale", "step": "STEP_VALENCE_GAIN", "weight": "W_RULE_VALENCE"},
    {"name": "meta_confidence_into_signal", "signal": "meta_confidence_mean", "cmp": "<",
     "thr": "THR_META_CONF", "module": "reflection_policy", "target": "W_META_CONFIDENCE",
     "kind": "const_add", "step": "STEP_W_META", "weight": "W_RULE_META"},
    {"name": "weak_advantage_normalized_outer", "signal": "advantage_abs_mean", "cmp": "<",
     "thr": "THR_ADVANTAGE", "module": "plasticity_policy", "target": "hebbian_delta",
     "kind": "swap_call", "old": "np.outer", "new": "_normalized_outer", "step": None,
     "weight": "W_RULE_SWAP_OUTER"},
    {"name": "weak_advantage_novelty_term", "signal": "advantage_abs_mean", "cmp": "<",
     "thr": "THR_ADVANTAGE", "module": "reflection_policy", "target": "reflection_signal",
     "kind": "insert_term", "arg": "novelty", "step": "STEP_W_NOVELTY", "weight": "W_RULE_NOVELTY_TERM"},
    {"name": "reflection_error_flood", "signal": "reflection_error_rate", "cmp": ">",
     "thr": "THR_REFLECTION_ERRORS", "module": "reflection_policy", "target": "LOW_QUALITY_THRESHOLD",
     "kind": "const_scale", "step": "STEP_QUALITY_THRESHOLD", "weight": "W_RULE_QUALITY_THR"},
    {"name": "bayes_reorder_forgetting", "signal": "bayes_abs_err", "cmp": ">",
     "thr": "THR_BAYES_ABS_ERR", "module": "bayes_policy", "target": "beta_update",
     "kind": "reorder", "index": 0, "step": None, "weight": "W_RULE_REORDER"},
]


def urgency(value, cmp, thr):
    """Relative exceedance of a signal past its threshold (0 when not triggered)."""
    scale = abs(thr) + 1e-9
    ex = (value - thr) / scale if cmp == ">" else (thr - value) / scale
    return ex if ex > 0 else 0.0


def rule_score(weight, value, cmp, thr, consecutive_rejects):
    """Priority of a rule given the incumbent's signal value and its reject streak."""
    u = min(urgency(value, cmp, thr), URGENCY_CAP)
    if u <= 0.0:
        return 0.0
    return weight * u - TABU_PENALTY * consecutive_rejects
