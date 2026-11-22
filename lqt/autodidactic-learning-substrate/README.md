# Theorem-Driven Autodidactic Substrate

This working substrate keeps the existing C++ LQT/RTA/RWA runtime open and uses
`autodidactic_learning.py` as the Auto/train loop.

## Core boundary

- RTA is structural attention: it selects which knowledge entities receive
  computation.
- RWA is recursive weight/state storage: it carries representations, recursive
  references, phase/error state, and evolution history.
- LQT remains the parameter/value container and C++ runtime boundary. This
  Python file does not replace or import the C++ implementation.

## Theorem routing

| Stage | Authority | Runtime responsibility |
|---|---|---|
| Attention | RTA boundary | Select relevant structure before synthesis |
| Recursive state | RWA boundary | Store/evolve recursive representations |
| Transform | RAL | Move between abstraction levels with coherence checks |
| Belief | RBUS | Update bounded evidence/posterior state |
| Monitor | URSMIF | Detect contradiction and recursive instability |
| Stability | RAL–RSRE bridge | Apply intervention and stability gates |
| Control | RLA | Run bounded cycles and checkpoint progress |
| Validation | RAL bridge | Keep higher-order claims as validation targets |
| Motivation | RLM | Leave goal/value formation as an experience-driven adapter |

The seven source papers are kept under `theorems/` and are loaded as authority
metadata. Their presence is checked each cycle; the code does not claim that
the papers' full mathematical proofs are already implemented.

## Current train-cycle contract

`run_training_cycle()` executes:

`RTA attention -> RWA recursive state -> RAL transform -> RBUS update -> URSMIF monitor -> RAL-RSRE stability gate -> RLA checkpoint`

The content boundary now uses a deterministic, parameter-free encoder instead
of silently injecting random content vectors. Native recursive-weight and
`.rw` persistence modules remain optional adapters.

## Remaining implementation work

1. Connect a real content/embedding provider for production-quality semantic
   representations.
2. Implement the native `.rw` serializer/loader contract and test it against
   the C++ runtime; the current fallback retains RWA state in a registry only.
3. Add theorem-specific numerical tests for convergence, contradiction
   intervention, and abstraction coherence.
4. Run the full system in the user's environment where PyTorch and the native
   recursive-weight modules are available.
