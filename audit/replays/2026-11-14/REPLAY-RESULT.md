# Ramtastic replay — 2026-11-14

## Verdict
Original unmodified release build: **FAIL**, exit code 1. The known build defect was reproduced.
Separate disclosed diagnostic build: **PASS**. This does not make the original release a passing build.

Target: `enuminous/Ramtastic` at `916ab476012852778edd9ca63aecf200a8e90ed1`.
Lean: `4.30.0-rc1`, commit `714601baf118066cbf3f282361339c6d06665b2a`.
Lake: `5.0.0-src+714601b`. Recorded manifest and toolchain remained unchanged.

## Execution
Fresh disposable checkout; official toolchain installed locally. Cache fetching encountered a read-only home path, resolved with workspace-local XDG_CACHE_HOME, and HTTP 429 rate limits. Missing pinned dependencies were compiled locally. An environment restart interrupted compilation; its log was preserved and `lake build` resumed using the same source and dependency pins. No project tracked edits preceded the original failure.

`lake build` failed in `Ramtastic/Dolbeault/DolbeaultTheorem.lean` with unknown `DelDelBar.del` / `DelDelBar.delbar` identifiers (lines 62–79) and consequent unsolved goals.

After recording the failure, the published diagnostic script opened `Ramtastic.ComplexStructure` and replaced the zero-form proof with its disclosed simplification. Patched build passed (3434 jobs).

Checks:
- Audit bundle integrity: 51 files passed (earlier phase).
- Python audit reproduction and 22 engine tests passed (earlier phase).
- Released-subset axiom audit: 2221 safe declarations, 926 theorems, 0 unsafe.
- Four rejection controls passed: public axiom, private axiom, placeholder/sorryAx, native proof.
- Diagnostic full axiom audit: 2223 safe declarations, 928 theorems, 0 unsafe.
- Five semantic probes compiled with warnings as errors; dependencies limited to printed standard Lean axioms.

## Interpretation
This is a retrospective known-result replay, not a blinded experiment, new discovery, commissioned audit, or validation of EFMW physics or general audit efficacy. The patched proof does not address all semantic applicability limitations.

Logs and exact patch are in `run/results`; interrupted and resumed original build logs are preserved separately. At completion of the run, no publication or external communication had occurred. This publication is a later packaging step.

## Public evidence packaging

Absolute execution-workspace/home paths and the ephemeral hostname are normalized in this public copy. Compiler diagnostics, source/dependency pins, counts and verdicts are unchanged. The original run was interrupted and resumed; `continue.sh` records an attempted continuation, not a claim that every command in it completed as one uninterrupted script.

- [Evidence directory](run/results/)
- [Original failure log](run/results/frozen-build-resumed.log)
- [Diagnostic patch](run/results/diagnostic.patch)
- [Diagnostic build](run/results/diagnostic-build.log)
- [Environment](environment.txt)
- [Public evidence archive](replay-evidence-public.tar.gz)
- [Checksums](SHA256SUMS.txt)

Original source attribution remains with the Ramtastic authors; this replay does not establish independent scientific validation.
