"""Pre-registered constants of the self-modification gate.

Fixed before the first generation ran (see PREREGISTRATION.md; the baseline
replicate-noise measurement that sets MIN_DELTA is written to run.json first). The loop
cannot edit this file (protected by gate.py).
"""

from __future__ import annotations

# ---------------------------------------------------------------- evaluation protocol
N_TRAIN = 12                 # training steps per seed (full loop: learn + self-modify)
N_HELDOUT = 10               # held-out steps per seed (prequential: scored before update)
SELECT_SEEDS = (0, 1, 2, 3, 4)  # used during selection
FINAL_SEEDS = (1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007)  # never used during selection
HIDDEN_DIM = 64
SEQ_LEN = 4
METACOG_STATE_DIM = 64
LQT_BACKEND = "python"       # pinned: another lane may flip the default backend

# Corpus pools by passage index (load_corpus order): train / selection held-out /
# final held-out. Final held-out passages are never seen during selection.
POOL_TRAIN = (1, 2)          # index % 4 in POOL_TRAIN
POOL_SELECT_HELDOUT = (3,)
POOL_FINAL_HELDOUT = (0,)

# ---------------------------------------------------------------- objective
# J_seed = -NLPD_heldout + LAMBDA_Q * reflection_quality_heldout
#   NLPD_heldout: mean over held-out steps and the three loop beliefs
#     (reflection.quality, reflection.meta_confidence, ethics.alignment) of
#     -log Beta(x_t | alpha_t, beta_t) where (alpha_t, beta_t) is the belief BEFORE
#     the step's update and x_t the step's observed evidence (clipped to
#     [EPS_CLIP, 1-EPS_CLIP]); each term capped at NLPD_CAP.
#   reflection_quality_heldout: mean engine quality_score on held-out passages
#     (metacognitive_analyzer output; read-only engine code).
LAMBDA_Q = 10.0
NLPD_CAP = 50.0
EPS_CLIP = 1e-3

# ---------------------------------------------------------------- acceptance rule (live runs)
# Each generation: one proposed edit, applied in an isolated candidate copy; the live
# cognition loop runs the candidate on the fixed seeds and on FRESH_PER_GEN fresh seeds
# (unique to the generation, never reused), and the incumbent on the same fresh seeds.
# Keep the edit iff the system's own metric goes up: mean fixed-seed dJ > MIN_DELTA with
# dJ > 0 on >= MIN_SEEDS_IMPROVED fixed seeds, mean fresh-seed dJ > 0, and every run
# stays healthy (guards below).
FRESH_PER_GEN = 2
FRESH_SEED_BASE = 100_000    # fresh seeds: FRESH_SEED_BASE + FRESH_PER_GEN*gen + k
MIN_DELTA_FLOOR = 0.01       # MIN_DELTA = max(floor, 3 * baseline replicate max |dJ|)
MIN_SEEDS_IMPROVED = 4       # of len(SELECT_SEEDS) = 5
# guards (per seed): the run itself must stay healthy
DW_COLLAPSE_FLOOR = 1e-12    # mean |dW| over training steps must exceed this
W_NORM_RATIO_MAX = 10.0      # ||W_end|| / ||W_start|| for every Psi matrix
# IALA learned count may not fall below the incumbent's (no learning regression)

# ---------------------------------------------------------------- IALA ethics filter
# Operator approval (Daeron, 2026-11-21, "IALA yes"): loosen the filter so the loop's
# theorem passages are learned. Keyword features are 0 for ~89% of passages; with the
# original rule (neutral_prior 0, threshold 0.5) 0/544 passages were accepted.
# neutral_prior 0.5 / threshold 0.35: neutral text passes (0.5*0.8*1.0 = 0.40 > 0.35);
# passages whose mean archetype alignment is below about -0.06 (net harm/deception/
# bias/control/cruelty language, ~5% of the corpus) are still rejected.
# NOT editable by the loop: the filter is an ethics invariant, not a tuning knob.
IALA_FILTER = {"acceptance_threshold": 0.35, "neutral_prior": 0.5}

# ---------------------------------------------------------------- gate runtime
EVAL_TIMEOUT_S = 600         # per candidate evaluator subprocess (2 cores shared)
MAX_META_DEPTH = 1           # proposer_policy edits may not themselves trigger meta edits
ALLOWED_EDIT_PREFIX = "cognition/mutable/"
MUTABLE_MODULES = ("bayes_policy", "plasticity_policy", "reflection_policy",
                   "motivation_policy", "proposer_policy")
OBJECT_MODULES = ("bayes_policy", "plasticity_policy", "reflection_policy", "motivation_policy")
ALLOWED_IMPORTS = ("math", "numpy")
