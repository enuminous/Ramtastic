# Verification evidence — 2026-10-16

**The original release fails. The disclosed diagnostic checkout passes.**
These are separate compiler observations, not interchangeable claims.

Target: `916ab476012852778edd9ca63aecf200a8e90ed1`. Toolchain:
`leanprover/lean4:v4.30.0-rc1`. Mathlib:
`8ec19128ad27190c2ec7c872d504be0a2877bd68`. Both dependency files and the
toolchain file were checked unchanged after execution.

## Original source

[Frozen build run](https://github.com/enuminous/Ramtastic/actions/runs/38963360333),
job `117183670827`, audit commit `8fac53601d33aeabd0e4753380992ea0bd4102d4`:
`lake build` failed on unresolved `DelDelBar.del` and `DelDelBar.delbar` in
`Ramtastic/Dolbeault/DolbeaultTheorem.lean`, starting at line 62.
The remaining 75 non-root modules compiled. See [frozen-build.log](frozen-build.log).
The original root cannot receive a successful whole-release kernel certificate.

## Successful diagnostic and adversarial checks

[Successful exact-toolchain run](https://github.com/enuminous/Ramtastic/actions/runs/38967875726), job `117198752732`,
audit commit `c899a756f5f74476491adbf624f603b84d59d1c0`. Full captured output:
[verified-diagnostic.log](verified-diagnostic.log).

| Check | Observed result |
|---|---|
| Diagnostic full build | Passed, all 77 released modules included |
| 75 unchanged modules, compiled axiom scan | Passed: 2,221 safe declarations, 926 theorem declarations, 0 unsafe |
| Full diagnostic checkout, compiled axiom scan | Passed: 2,223 safe declarations, 928 theorem declarations, 0 unsafe |
| Unused public axiom control | Rejected for an unapproved axiom |
| Unused private axiom control | Rejected for an unapproved axiom |
| `sorry` control | Rejected for `sorryAx` |
| `native_decide` control | Rejected for its generated `AuditProbe.probe._native.native_decide.ax_…` axiom |
| Five Lean probe theorems, covering four witnesses | Passed with warnings treated as errors |
| Dependency pin preservation | Passed |

The 75-module scan imports only original, unmodified modules. It excludes the
failed Dolbeault theorem module and the root. Its evidence therefore does not
depend on the diagnostic proof correction. The full scan additionally covers
the corrected module. Both scans include private declarations and permit only
`propext`, `Classical.choice` and `Quot.sound`. The compiled theorem counts
include generated helper/equational declarations; the independent lexical count
of source-written `theorem`/`lemma` declarations is 373.

The diagnostic opens `Ramtastic.ComplexStructure` and replaces only the proof
body of `deRham_to_dolbeault` with a direct simplification of the projections,
pullback and closed-form hypothesis. The theorem statement is unchanged.
[diagnostic-source.patch](diagnostic-source.patch) and
[diagnostic_namespace.py](diagnostic_namespace.py) show the exact intervention.
The script first checks that the input source is byte-identical to the frozen
Git object. The patch is applied only in a disposable execution checkout;
the published original mathematical files remain unchanged.

The five probe theorems certify: an actual bare `Hinge` need not preserve
Euclidean length; its actual quarter-turn changes that length; the vacuous
sheaf field admits unequal dimensions; the clamped and bounded sums differ;
and two skew-adjoint square-minus-identity matrices can have a non-self-adjoint
product. These witness unrestricted scope/specification defects. They do not
refute the conditional rotation group law or a theorem with added
skew-adjointness/inner-product hypotheses.

## Retained failures and corrections

| Run | Result and interpretation | Captured log |
|---|---|---|
| [38963360333](https://github.com/enuminous/Ramtastic/actions/runs/38963360333) | Original source elaboration failure | `frozen-build.log` |
| [38963899857](https://github.com/enuminous/Ramtastic/actions/runs/38963899857) | Shallow checkout lacked the frozen Git object; audit setup error | `diagnostic-setup-failure.log` |
| [38965312902](https://github.com/enuminous/Ramtastic/actions/runs/38965312902) | Namespace-only correction left two zero-form proof goals | `namespace-only-failure.log` |
| [38965836165](https://github.com/enuminous/Ramtastic/actions/runs/38965836165) | First zero-form rewrite attempt failed to match projection simplification | `zero-rewrite-failure.log` |
| [38966396070](https://github.com/enuminous/Ramtastic/actions/runs/38966396070) | Diagnostic build passed; private Lean API and probe tactic errors in audit code | `audit-harness-failure.log` |
| [38967005688](https://github.com/enuminous/Ramtastic/actions/runs/38967005688) | Both axiom scans passed; native-name expectation and probe reduction needed correction | `probe-harness-failure.log` |
| [38967875726](https://github.com/enuminous/Ramtastic/actions/runs/38967875726) | All diagnostic checks passed | `verified-diagnostic.log` |

Failed audit-code runs are not additional mathematical defects in Ramtastic.
Their error-recovery `sorryAx` output is retained transparently and does not
mean that the original author wrote a `sorry` proof.

## Python and package reproduction

Fresh clones at all three recorded commits reproduced the inventory, four
exact witnesses, 46 conformance adapter outputs, 90 numerical comparisons,
22 engine tests and extension Python source-certificate generators. Generated
JSON matched the shipped bytes. See [fresh-reproduction.json](fresh-reproduction.json)
and [fresh-reproduction.log](fresh-reproduction.log). That local reproduction
did not run Lean; the exact-toolchain Lean evidence is the hosted run above.
Generated extension Lean certificates were not newly compiled in this audit.

The final archive builder checks flat root-only filenames, uniqueness and ZIP
CRC integrity, and emits SHA256 checksums. Run `python3 reproduce.py --verify-only`
after extraction. A full fresh Python reproduction and an optional exact-pin
Lean reproduction are documented in [README.md](README.md).

The bundled [workflow](zoo-audit.yml) matches the
[published diagnostic workflow](https://github.com/enuminous/Ramtastic/blob/c899a756f5f74476491adbf624f603b84d59d1c0/.github/workflows/zoo-audit.yml).
The axiom collector uses the pinned toolchain's public
[`Lean.collectAxioms` API](https://github.com/leanprover/lean4/blob/v4.30.0-rc1/src/Lean/Util/CollectAxioms.lean).
