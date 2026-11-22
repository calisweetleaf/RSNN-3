"""Psi-operator plasticity (reward-modulated Hebbian) for the self-modification step.

Moved from runtime/loop.py step 6 (rosemary-runtime lane's integration choice):

    dW_k = eta * drive * (1 - severity) * advantage * outer(psi_eth, region_k)

Defaults reproduce it exactly (ETA = LoopConfig.eta default 0.05, SEVERITY_GATE = 1).
``_normalized_outer`` and ``_sign_outer`` are alternative operators the proposer may
swap in for ``np.outer`` inside ``hebbian_delta``.
"""

import numpy as np

ETA = 0.05            # base self-modification rate
SEVERITY_GATE = 1.0   # how strongly sentinel contradiction severity suppresses plasticity


def modification_scale(drive, severity, advantage):
    """Scalar gain of the Hebbian update for one step."""
    return ETA * drive * (1.0 - SEVERITY_GATE * severity) * advantage


def hebbian_delta(post, pre, scale):
    """Weight change for one Psi integration matrix (shape len(post) x len(pre))."""
    return scale * np.outer(post, pre)


def _normalized_outer(a, b):
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    return np.outer(a, b) / (na * nb + 1e-12)


def _sign_outer(a, b):
    return np.outer(np.sign(a), np.sign(b)) * float(np.mean(np.abs(a))) * float(np.mean(np.abs(b)))
