# Ramtastic — full Monolithic Zoo audit

**2026-10-16 · Prepared for Matthew Chenoweth Wright / eNuminous**

**Verdict: useful formal mathematics with a reproducible release build defect,
two concrete specification defects, and documentation that exceeds the proved
scope.** No evidence here establishes an unconditional solution to the Hodge,
BSD, twin-prime or Yang–Mills problems, or the unreleased halting construction.
Several source files explicitly describe their statements as requirements or
conditional interfaces; this audit preserves that distinction.

The frozen release is [916ab476](https://github.com/enuminous/Ramtastic/tree/916ab476012852778edd9ca63aecf200a8e90ed1),
a fork of [CasimirKnights/Ramtastic](https://github.com/CasimirKnights/Ramtastic).
Source attribution remains C. Forrester (Adauriel), with the formalization
credits recorded in individual files. This is an EFMW audit of that work, not
a claim that EFMW produced its theorems.

## Concurrent Aristotle summary

During publication, commit `df74289123e82a42be5d31f40038552bbb6b38a6`
added `ARISTOTLE_SUMMARY.md` to main. It reports a separate `RequestProject`
Bass/Clifford formalization and the same self-adjointness correction. That
commit adds only the summary; its referenced Lean files are absent. The summary
is preserved alongside this audit. See [PUBLICATION-ADDENDUM.md](PUBLICATION-ADDENDUM.md)
for the scope distinction. The executed audit remains pinned to the earlier
84-file release; the new summary is not counted as verified Lean code here.

## What was covered

| Coverage | Result |
|---|---|
| Frozen tracked files | 84, individually SHA256-hashed |
| Released Lean modules | 77, including the root; all reachable from the root |
| Source-written theorem/lemma declarations | 373: 371 `theorem` and two `lemma`; generated declarations excluded |
| Structure/class declarations | 85, inventoried with their fields |
| Canonical Zoo | All 46 fixed operations reviewed; all 46 selected Python adapters executed on published conformance fixtures |
| Numerical port comparisons | 90/90 within the frozen 1e-12 tolerance |
| Engine tests | 22/22 passed |
| Actual target adapters | WEASEL and ELEPHANT executed on explicitly defined audit inputs; 44 lack their required target observations |
| Extensions | All five reviewed; CIRCUS returns FAIL for the broad documentation/specification gate; MONSTER returns N/A; three require unavailable data |
| Adversarial witnesses | Four exact rational/integer witnesses, with corresponding Lean probes |

The [complete operation ledger](ZOO-46.md), [input schemas](operation-catalogue.json),
[inputs](target-operation-inputs.json), [outputs](target-operation-results.json),
and [extension ledger](extension-ledger.json) make the scope inspectable.
**A fixture run is a software check, not an application to the target theorem.**
There is no honest way to supply 44 missing empirical datasets merely by naming
the animals. No overall scientific score or invented benchmark is reported.

The current formal Zoo source is pinned to `15dfb335424e77e1458cd77996f23d074dac0d88`.
The Python adapter engine is pinned to `6fbd8beddf442e7adb752ec30ae054a25857602b`
and retains its older Zoo snapshot. Both hashes are recorded per operation;
this audit does not claim complete Python/Lean pipeline equivalence.

## Reproducibility and kernel status

The unmodified release **fails `lake build`** with its own Lean
`v4.30.0-rc1` and Mathlib `8ec19128ad27190c2ec7c872d504be0a2877bd68`.
[The original hosted run](https://github.com/enuminous/Ramtastic/actions/runs/38963360333)
reports unresolved `DelDelBar.del` and `DelDelBar.delbar` names in
`Ramtastic/Dolbeault/DolbeaultTheorem.lean`, beginning at line 62. This is a
source elaboration failure, not a download failure or counterexample to the
intended mathematical statement. The whole-release axiom audit was consequently
blocked in that run.

The namespace-only diagnostic exposed two further unsolved zero-form goals.
The final diagnostic opens `Ramtastic.ComplexStructure`, unfolds the projection
and pullback definitions, and rewrites the closed-form hypothesis in a
disposable checkout. The theorem statement is unchanged. Its result,
complete counts, rejection controls and exact run links are recorded in
[VERIFICATION.md](VERIFICATION.md). The final hosted run passed the build,
both axiom scans, four rejection controls and five Lean probe theorems.
The unchanged 75-module subset has 2,221 compiled safe declarations; the
full diagnostic checkout has 2,223. Neither scan found unsafe declarations
or dependencies beyond the three allowed foundational axioms.
**The published mathematical source is not silently repaired.** A successful
diagnostic build certifies the modified checkout, not the frozen release.

The strict audit traverses compiled project declarations, including private
ones, and permits only `propext`, `Classical.choice`, and `Quot.sound`.
It tests rejection of unused public/private axioms, a `sorry` proof and native
proof evaluation. This follows Lean's [proof-validation guidance](https://lean-lang.org/doc/reference/latest/ValidatingProofs/).
“No custom axioms” still permits theorem hypotheses and structure proof fields:
it is not a certificate that those fields have been constructed for a real
geometric or physical object.

## Exact findings

| ID | Finding | Evidence status and scope |
|---|---|---|
| F00 | The frozen release does not build. | **Demonstrated** by hosted exact-pin compiler errors. |
| F01 | `Hinge` alone does not imply Euclidean isometry or circular Euclidean orbits. | **Demonstrated boundary.** This does not refute Bass (i) with its additional skew-adjointness assumption. |
| F02 | The prose rule “skew × skew = self-adjoint” needs a commutation hypothesis. | **Rejected as unrestricted prose.** Exact anticommuting skew-adjoint 4×4 matrices give a non-self-adjoint product. |
| F03 | `StructureSheafWithHodge.hodge_symmetry_0q` ends in `∨ True`. | **Demonstrated specification defect.** The field imposes no constraint; the source itself notes the missing full statement. |
| F04 | `RationalHodgeStructureData.hodge_deRham` clamps indices with `min`. | **Demonstrated specification defect.** It adds out-of-range entries instead of excluding them. |
| F05 | Named prime/Hodge/BSD endpoints often consume the claimed conclusion or a deep prerequisite as input. | **Demonstrated conditional scope**, not an unsound proof or a new global axiom. |
| F06 | The projective-space example defines `CPn n := Unit`, with separately supplied algebraic data. | **Demonstrated model boundary.** No equivalence to geometric complex projective space is established by that definition. |
| F07 | The Tower strong BSD surface existentially chooses positive period/Sha-order/Tamagawa values. | **Supported but incomplete** as the classical statement: those witnesses need identification with the actual arithmetic invariants. |
| F08 | QuantumYM transfer theorems assume a uniform finite-level gap and transfer/compatibility data. | **Demonstrated conditional scope**; the published bounded-operator infrastructure does not construct a nontrivial 4D quantum Yang–Mills theory. |
| F09 | Bass has six named theorems plus a structure and a definition. | **Demonstrated documentation mismatch** with the eight-theorem wording. |
| F10 | No halting-construction theorem was located in the released inventory. | **Unresolved/outside supplied artifact.** The root explicitly excludes the private Vega root; no claim is made about unavailable code. |

**F01, exact witness.** On a real two-dimensional space, take

\[
J=\begin{pmatrix}0&-2\\1/2&0\end{pmatrix}.
\]

Then \(J^2=-I\), so it inhabits the actual `Hinge` structure. But the Euclidean
squared length of \((1,0)\) changes from \(1\) to \(1/4\) under the quarter-turn
`rotate h (π/2) = J`. The group law remains valid. To obtain Euclidean rotations,
carry and prove inner-product compatibility. The README's stated skew-adjoint
Clifford-action hypothesis supplies relevant extra structure; the bare `Hinge`
does not encode it.

**F02, exact witness.** The files supply two real skew-adjoint quaternion-action
matrices, each squaring to \(-I\). They anticommute and their product is nonzero
skew-adjoint. In general \((AB)^*=BA\) for skew-adjoint \(A,B\), so self-adjointness
requires \(AB=BA\). This attacks the unrestricted table entry, not `rotate_add`.

**F03, exact witness.** Cohomology dimensions `[1, 7]` satisfy the existing field
through `Or.inr True.intro`. There is no constraint on the missing companion
\(H^0(X,\Omega^q)\) dimension. Replacing the field with equality to `cohomDim 0`
would also be the wrong repair: the intended two distinct cohomology objects
must be represented.

**F04, exact witness.** For dimension two and degree three, use the symmetric
nonnegative Hodge-number fixture
`[[1,0,1],[0,20,0],[1,0,1]]`. The bounded diagonal sum is zero; the implemented
clamped sum is two because it includes `(0,2)` and `(2,0)`. This finite witness
does not claim to construct a geometric surface. It rejects the claimed
identity between the two sum formulas.

All four witnesses and controls are in [counterexamples.json](counterexamples.json)
and [SemanticProbes.lean](SemanticProbes.lean). WEASEL only filters these supplied
findings under a one-key perturbation budget; it did not discover them.

## What survives, and what remains to prove

The rotation group law, angle identities, Clifford relations, finite Schur
inequality, quotient/algebra manipulations, measure constructions and explicitly
conditional spectral-transfer arguments are useful mathematical content within
their stated types. The [module review](SOURCE-REVIEW.md) records which conclusions
are genuine constructions and which require supplied proof fields.

Examples of the latter are `hodge_from_chain`, which returns its `h_hodge`
argument; `TwinPrimes.Tower.twinPrimes`, which extracts a `twin_primes` field;
and the rank-zero/rank-one BSD helpers, which use Kolyvagin/Gross–Zagier facts
stored in `KGZData`. These are legitimate interfaces, not independent proofs
of their assumptions. The Hardy–Littlewood row structure assumes arbitrarily
large pairs but contains no asymptotic ratio limit; its positive singular-series
field is not what proves infinitude.

The familiar square-minus-identity/trigonometric group law and Clifford
relations are **equivalent/adjacent to established mathematics**. Mathlib already
contains [Clifford square and orthogonality identities](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/CliffordAlgebra/Basic.html).
New packaging or formalization work may be valuable; no new mathematical or
physical law follows from renaming these identities. The broader architectural
claim that all analytical machinery follows from circles is **unresolved**, and
the unrestricted self-adjointness shortcut is refuted above. The [official
Yang–Mills problem](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf)
requires existence and a mass gap for a nontrivial quantum theory on four-space,
which is substantially more than the supplied conditional operator statements.

## Independence and next acceptance tests

This was a retrospective audit. The first source inspection preceded the
[frozen plan](PLAN.md); additional discovered checks are recorded as exploratory.
Python witnesses and Lean probes check the same constructed examples, so they
are cross-implementation verification, not independent scientific experiments.
Zoo reference expectations originate in the same upstream project as the ports.
No AI intent, product performance, physical correspondence or undisclosed result
is inferred from source names or comments.

1. Apply the namespace/zero-form repair as a separately reviewed source change; require
   an unmodified clean checkout to build and pass the full axiom audit.
2. Replace the vacuous sheaf field with the correct companion cohomology data;
   require a meaningful symmetry theorem and a failing test for inconsistent data.
3. Replace clamping with a bounded-index sum; require the degree-three fixture
   above to evaluate to zero and verify boundary degrees independently.
4. Separate theorem hypotheses, construction witnesses and scientific claims in
   the catalogue. Require concrete instances before promoting an interface to a
   theorem about a particular variety, curve or physical theory.
5. For the halting claim, supply the exact theorem constant, all definitions,
   full dependency closure and commit. Audit its quantifiers and computability
   assumptions against the claimed informal statement before judging it.

The completion of this **audit** does not close the missing target data or these
mathematical construction obligations.
