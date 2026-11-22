"""RLDIS-style loop detection over the self-modification history (protected).

Maps the RLDIS v1.1 detection classes (sec. 2.3) and URSMIF v1.5 pattern definitions
(sec. 2.1) onto edit histories:

* Simple repetition (URSMIF 2.1.1, sim > theta_rep with theta_rep = 1): a candidate whose
  full mutable-surface hash equals any state already accepted (including the baseline)
  is a revisit -> rejected before evaluation ("cycle").
* Contradiction spiral (RLDIS 2.3; URSMIF 2.1.2 density): an accepted-edit history in
  which the same (module, target) flips direction >= OSC_FLIPS times -> target frozen.
* Explicit loop rejection (RLDIS 3.1.2): the same edit signature rejected
  >= REJECT_LIMIT times -> tabu for TABU_GENS generations.
* Stagnation (Eigenrecursion 5.3 attractive fixed point): STALL_GENS generations without
  an acceptance -> flagged as a suspected fixed point of the gated operator (logged;
  the run continues to its generation budget with exploration).
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Optional

OSC_FLIPS = 2
REJECT_LIMIT = 3
TABU_GENS = 5
STALL_GENS = 10


def signature(p: Dict[str, Any]) -> str:
    kind = p["kind"]
    if kind in ("const_scale",):
        direction = "up" if p["factor"] > 1 else "down"
    elif kind in ("const_add", "insert_term"):
        v = p.get("delta", p.get("coef", 0.0))
        direction = "up" if v > 0 else "down"
    elif kind == "const_set":
        direction = "set"
    elif kind == "swap_call":
        direction = f'{p["old"]}->{p["new"]}'
    else:
        direction = f'idx{p.get("index")}'
    return f'{p["module"]}.{p["target"]}:{kind}:{direction}'


class LoopDetector:
    def __init__(self):
        self.accepted_states: Dict[str, int] = {}      # surface hash -> generation
        self.accepted_dirs: Dict[str, List[str]] = defaultdict(list)
        self.rejects: Dict[str, int] = defaultdict(int)
        self.tabu_until: Dict[str, int] = {}
        self.frozen: set = set()
        self.last_accept_gen = 0

    def register_state(self, surface_hash: str, gen: int) -> None:
        self.accepted_states.setdefault(surface_hash, gen)

    def precheck(self, proposal: Dict[str, Any], surface_hash: str, gen: int) -> Optional[str]:
        """Reason to refuse a candidate before evaluation, or None."""
        key = f'{proposal["module"]}.{proposal["target"]}'
        if key in self.frozen:
            return f"RLDIS contradiction spiral: {key} frozen after {OSC_FLIPS} direction flips"
        sig = signature(proposal)
        if self.tabu_until.get(sig, -1) >= gen:
            return f"RLDIS explicit loop rejection: {sig} tabu until gen {self.tabu_until[sig]}"
        if surface_hash in self.accepted_states:
            return f"RLDIS repetition: candidate surface == accepted state of gen {self.accepted_states[surface_hash]}"
        return None

    def is_blocked(self, proposal: Dict[str, Any], gen: int) -> bool:
        key = f'{proposal["module"]}.{proposal["target"]}'
        return key in self.frozen or self.tabu_until.get(signature(proposal), -1) >= gen

    def record(self, proposal: Dict[str, Any], accepted: bool, gen: int, surface_hash: Optional[str]) -> Dict[str, Any]:
        sig = signature(proposal)
        key = f'{proposal["module"]}.{proposal["target"]}'
        events = {}
        if accepted:
            self.last_accept_gen = gen
            self.rejects[sig] = 0
            if surface_hash:
                self.register_state(surface_hash, gen)
            d = sig.rsplit(":", 1)[1]
            hist = self.accepted_dirs[key]
            hist.append(d)
            flips = sum(1 for a, b in zip(hist, hist[1:]) if a != b and {a, b} == {"up", "down"})
            if flips >= OSC_FLIPS:
                self.frozen.add(key)
                events["frozen"] = key
        else:
            self.rejects[sig] += 1
            if self.rejects[sig] >= REJECT_LIMIT:
                self.tabu_until[sig] = gen + TABU_GENS
                self.rejects[sig] = 0
                events["tabu"] = {sig: self.tabu_until[sig]}
        if gen - self.last_accept_gen >= STALL_GENS:
            events["stagnation"] = f"no acceptance for {gen - self.last_accept_gen} generations (suspected fixed point)"
        return events

    def state(self) -> Dict[str, Any]:
        return {"frozen": sorted(self.frozen), "tabu_until": dict(self.tabu_until),
                "reject_streaks": {k: v for k, v in self.rejects.items() if v},
                "accepted_states": len(self.accepted_states)}
