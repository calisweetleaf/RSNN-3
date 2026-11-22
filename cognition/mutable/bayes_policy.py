"""Beta-belief evidence policy for runtime.bayesian_config_orchestrator.

RecursiveBayesianUpdater.recursive_update re-applies the same observation at every
recursion depth until the parameter change falls below 1e-6 or max depth is hit
(RBUS, Bayesian_Updating_System.md 3.1.1 ``update_beliefs`` recurses with the same
``evidence``). With a constant weight per depth one observation is counted
``max_depth`` times (10 x 10 pseudo-counts in the loop's config), so beliefs harden
far faster than the evidence warrants.

Defaults below reproduce that original behaviour exactly:
  pseudo-counts per depth = PSEUDO_COUNT_SCALE * DEPTH_DECAY ** depth, DEPTH_DECAY = 1
  no forgetting (FORGETTING = 1).
The self-modification loop may change these constants / this code under its gate.
"""

PSEUDO_COUNT_SCALE = 10.0   # original "Scale factor" in _update_beta_distribution
DEPTH_DECAY = 1.13055           # weight multiplier per recursion depth (1.0 = same evidence re-applied)
FORGETTING = 1.0            # retention of accumulated (posterior - prior) counts per observation


def evidence_weight(depth):
    """Pseudo-count weight of one observation at recursion ``depth``."""
    return PSEUDO_COUNT_SCALE * (DEPTH_DECAY ** depth)


def beta_update(alpha, beta, evidence, depth, prior_alpha, prior_beta):
    """Return the updated (alpha, beta) for evidence in [0, 1] at recursion ``depth``."""
    w = evidence_weight(depth)
    if depth == 0:
        alpha = prior_alpha + FORGETTING * (alpha - prior_alpha)
        beta = prior_beta + FORGETTING * (beta - prior_beta)
    new_alpha = alpha + evidence * w
    new_beta = beta + (1.0 - evidence) * w
    return new_alpha, new_beta
