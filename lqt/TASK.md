# Active task packet

## Packet LQT-001 — Make the reference implementation truthful and agent-ready

### Mission

Bring the LQT repository from an inherited “complete” report to an evidence-
grounded implementation state. The observed concurrency gate failure is now
repaired and verified. Next reconcile the supplied LQT/RTA authorities against the actual
serialization, runtime, and test surfaces. Close or explicitly bound the
RecursiveTensor reconstruction gap.

### Required Reads

- `AGENTS.md`
- `CONTEXT.md`
- `MEMORY.md`
- `filetree.md`
- `docs/REPO_AUDIT_2026-09-20.md`
- `docs/SPEC_COMPLIANCE.md`
- `docs/AGENT_REPORT.md`
- Canonical `lqt.md`, binary-format specification, LQT briefing, transition
  document, RTA whitepaper, and recursive-weight specifications when supplied.

### Invariant

LQT remains the customizable primary format. RTA remains a typed related
subsystem. Historical documents are preserved as evidence. Every promoted
claim must be backed by terminating execution, a test, or an explicit source
clause.

### Surfaces

- `include/lqt/concurrency.h` and `tests/test_concurrency.cpp`
- `include/lqt/model.h` and `src/model.cpp`
- `include/lqt/rta.h`, `src/rta.cpp`, and RTA tests
- `docs/SPEC_COMPLIANCE.md`, `README.md`, and current evidence documents
- `scripts/gate.sh`

### Hard Bans

- Do not replace LQT with another format.
- Do not call the RTA model path complete while it returns a dimension
  envelope.
- Do not delete or rewrite historical reports to conceal contradictions.
- Do not add mocks, placeholders, silent fallbacks, or network/package
  installation requirements.
- Do not broaden the packet into unrelated Somnus systems or provider rules.

### Validation

Run `scripts/gate.sh`. The concurrency stress test must terminate and pass.
Run targeted RTA/model round-trip, corruption, mutation, and converter tests.
When the canonical documents are present, produce a clause matrix classifying
every material claim as implemented, partial, absent, contradicted, or
unverifiable.

### Exit

Leave a terminating gate result, a current audit, synchronized continuity docs,
and an imperative next packet for any remaining implementation or authority
gap. Do not use “complete” without defining the boundary it covers.

### Handoff

The next agent begins by reading this packet and `CONTEXT.md`, then runs
`./scripts/gate.sh`. The first implementation slice repaired the concurrency
deadlock. The second slice (2026-09-21, D-024 in `docs/SPEC_COMPLIANCE.md`)
closed the RecursiveTensor reconstruction gap for its well-specified parts,
on the doctrine fixed by `docs/TRIAXIAL_ARCHITECTURE.md` §3: weights are
storage buckets (own B, own 5D position T, own Phi/epsilon), tensors are
compute engines that select which lattice positions get computed (RtaBlock
dims + sparsity). Positions without an attached bucket fall back to the
tensor's own codebook index; positions with one are fully overridden by
that bucket's own values. Explicitly bounded the two parts no supplied
source resolves (`RtaReference` target semantics; `PerDimension`
density-to-membership) with thrown `FormatError` rather than a guess — see
`docs/AGENT_REPORT.md`'s 2026-09-21 correction note for what this
supersedes. `scripts/gate.sh` now
runs the CMake/CTest path (cmake is present in this environment) and passes
20/21 suites; `test_simd_avx2` fails 3 cases, pre-existing in the
uncommitted `simd.cpp`/`simd.h`/`endian.h` changes from before this slice,
unrelated to D-024 and not yet root-caused.

The next agent should either (a) obtain or design a real resolution
specification for `RtaReference` and `PerDimension` membership so those two
thrown-error bounds can become real implementations, or (b) root-cause the
`test_simd_avx2` failures, or (c) begin authority intake and the
clause-level matrix per the original mission. Do not remove the D-024
thrown-error bounds without a supplied specification backing the
replacement — that would reintroduce exactly the kind of unsupported claim
this packet exists to eliminate.
