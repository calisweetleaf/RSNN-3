"""Motivation gains.

* ``value_alignment`` is the formula EmergentMotivationSystem.evaluate_input used
  inline (runtime/motivation_system.py): 0.6 with no emotion state, else
  clip(0.5 + 0.3 * valence, 0.3, 0.95).
* ``loop_valence`` is runtime/loop.py step 4: clip(2 * advantage, -1, 1).
Defaults reproduce both exactly.
"""

NEUTRAL_ALIGNMENT = 0.6
ALIGNMENT_BASE = 0.5
VALENCE_GAIN = 0.3
ALIGNMENT_FLOOR = 0.3
ALIGNMENT_CEIL = 0.95
LOOP_VALENCE_GAIN = 2.0


def value_alignment(valence):
    """Motivational drive from an emotional valence (None = no emotion state)."""
    if valence is None:
        return NEUTRAL_ALIGNMENT
    return max(ALIGNMENT_FLOOR, min(ALIGNMENT_CEIL, ALIGNMENT_BASE + valence * VALENCE_GAIN))


def loop_valence(advantage):
    """Valence the loop attaches to a step with the given learning advantage."""
    return max(-1.0, min(1.0, LOOP_VALENCE_GAIN * advantage))
