"""Reflection policy: how reflection scores become learning signals and errors.

Two consumers:

* cognition.cognitive_engine -- thresholds that turn base reflection into
  ``reflection_errors`` (MetaReflective path) and the gain of the runtime-weight
  mutation (MetaLearningBridge._modify_runtime_weight). Defaults are the literals the
  engine had before the move.
* runtime.selfmod.harness -- the reflection signal whose deviation from the Bayesian
  belief is the self-modification advantage. Default = quality_score only, which is
  what runtime/loop.py used (advantage = quality - prior mean of reflection.quality).

The reflection *scores* themselves (metacognitive_analyzer outputs) are computed by
read-only engine code; this module only decides how they are used.
"""

# --- engine reflection-error thresholds (cognitive_engine._perform_meta_reflection)
LOW_QUALITY_THRESHOLD = 0.6
ETHICAL_MISALIGNMENT_THRESHOLD = 0.7
CONSCIOUSNESS_INFLUENCE_FLOOR = 0.4
BLIND_SPOT_CONFIDENCE = 0.9
BLIND_SPOT_QUALITY = 0.7

# --- runtime weight mutation gain (MetaLearningBridge._modify_runtime_weight)
RUNTIME_WEIGHT_GAIN = 0.05

# --- reflection signal weights for the self-modification advantage
W_QUALITY = 1.0
W_NOVELTY = 0.0
W_ALIGNMENT = 0.0
W_CONFIDENCE = 0.0
W_META_CONFIDENCE = 0.0


def runtime_weight_strength(quality, avg_severity):
    """Mutation strength of the engine's runtime recursive weight."""
    return (1.0 - quality) * avg_severity * RUNTIME_WEIGHT_GAIN


def reflection_signal(quality, novelty, alignment, confidence, meta_confidence):
    """Scalar reflection signal compared against the belief baseline."""
    return (W_QUALITY * quality + W_NOVELTY * novelty + W_ALIGNMENT * alignment
            + W_CONFIDENCE * confidence + W_META_CONFIDENCE * meta_confidence)


def advantage(signal, baseline):
    """Learning advantage of this step relative to the belief baseline."""
    return signal - baseline
