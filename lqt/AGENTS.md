# LQT repository operator guide

## Mission

This repository is the customizable LQT reference implementation and its
evidence surface. It contains a C++17 binary container, reconstruction and
mutation machinery, RTA/recursive-weight subsystems, converters, examples, and
tests. The job of an arriving agent is to make the implementation agree with
the supplied authority and produce proof for every claim.

This is an implementation repository, not a generic agent framework. Keep the
control plane project-specific and keep the LQT/RTA boundary explicit.

## Authority and conflict handling

Use this order when artifacts disagree:

1. The current operator instruction in the active task packet.
2. Supplied canonical LQT documents and whitepapers, once present in the repo.
3. Executable behavior and tests in this repository.
4. `docs/SPEC_COMPLIANCE.md`, `docs/AGENT_REPORT.md`, and `README.md` as
   historical design and implementation records.

The archive currently contains no `lqt.md`, binary-format specification,
briefing, transition document, RTA whitepaper, or recursive-weight technical
spec. Do not call a claim whitepaper-verified until those sources are added and
checked. Do not overwrite historical reports to make them agree with a newer
run; record the contradiction in `docs/` and in the active state documents.

LQT is customizable. Do not freeze future work to the current v1.3 decisions
when a newer operator-supplied canon changes them. Preserve a deviation,
document the ruling, and add compatibility evidence.

RTA is a related subsystem, not an alias for all of LQT. Structural RTA block
serialization and standalone RTA/recursive-weight tests exist. The current
`LqtModel::reconstruct()` RecursiveTensor branch explicitly returns a dimension
envelope rather than a mathematically complete reconstruction. Treat that as a
known implementation gap until proven otherwise.

## Arrival route

Read in this order:

1. `TASK.md` — active packet and exit condition.
2. `CONTEXT.md` — current evidence and blockers.
3. `MEMORY.md` — durable vocabulary and boundaries.
4. `filetree.md` — semantic topology and ownership.
5. The required files named by the active packet.
6. Run `scripts/gate.sh` before changing implementation.

The gate is the repository's executable admission check. A missing CMake
installation is reported as an environment limitation; the direct GCC path is
the fallback and must not be mistaken for CMake/CTest validation.

## Working contract for a single agent

- Work from `main` unless the operator explicitly changes that instruction.
- Keep the change surface inside this repository.
- Preserve existing source, tests, examples, and historical reports unless a
  packet explicitly authorizes a repair.
- Do not add placeholders, mocks, silent fallbacks, or claims unsupported by a
  test or source document.
- When repairing a runtime defect, add or strengthen a regression test before
  declaring the gate green.
- When extending the format, update the binary decision register and add a
  round-trip or corruption test for the new bytes.
- When the whitepapers arrive, compare their clauses against headers, sources,
  tests, and serialized bytes; classify each as implemented, partial, absent,
  contradicted, or not verifiable.
- Update `CONTEXT.md`, `NOTEPAD.md`, `TASK.md`, and `filetree.md` when state,
  topology, or the next executable action changes.

## What each surface owns

| Surface | Ownership | Open it when |
| --- | --- | --- |
| `include/lqt/` | Public C++ data model, binary types, and API contracts | Changing or tracing an API or format field |
| `src/` | Runtime behavior and serialization implementation | Proving a mechanism or repairing behavior |
| `tests/` | Executable evidence, including negative and round-trip cases | Validating a claim or adding regression proof |
| `examples/` | Human-scale usage paths | Checking public API ergonomics |
| `docs/SPEC_COMPLIANCE.md` | Existing deviation and decision record | Reconciling format ambiguity |
| `docs/AGENT_REPORT.md` | Historical completion report | Comparing inherited claims with current evidence |
| `scripts/gate.sh` | Reproducible local acceptance gate | Every entry, implementation change, and handoff |
| `TASK.md` / `CONTEXT.md` / `NOTEPAD.md` | Active routing and continuity | Resuming or landing work |

## Exit requirements

An agent may mark a packet landed only when it has:

- run the strongest available gate and recorded exact results;
- separated passed, failed, skipped, blocked, and unverified checks;
- updated the affected docs and topology;
- left the next action imperative and executable;
- made no completeness claim beyond the evidence.
