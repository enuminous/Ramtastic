# Mathematical source review and proof obligations

The automated inventory covers all 77 released modules. The semantic review
below examines their central interfaces and endpoints; it is not a claim to
have independently rederived every one of the 373 source-written proofs.
Every exact source location and declaration header is in `source-inventory.json`;
all structure/class blocks are in `structure-fields.json`.

| Area | Modules | What is present | Obligation / boundary |
|---|---:|---|---|
| Bass | 1 | `Hinge`, `rotate`, six angle/group theorems | Inner-product compatibility and Clifford-to-hinge construction are not in this file. |
| BSD | 9 | Arithmetic/analytic data comparisons; rank, parity and product helpers; weak/strong statement definitions | Construct actual curve invariants and deep comparison fields. `KGZData` contains rank-zero/rank-one conclusions as inputs. Strong Tower witnesses must match actual periods/Sha/Tamagawa values. |
| ChowGroups | 6 | Free abelian cycles, quotients, rationalization, bilinear products, a truncated model | `VarietyData`/`RatEquivData` supply geometry. `CPn n := Unit` is a carrier label, not construction of projective space. |
| ComplexStructure | 4 | Almost-complex maps, projections, real/imaginary forms and differential identities | Smoothness/integrability and operator-domain hypotheses must remain explicit. |
| CycleClass | 5 | Cycle maps and a concrete rational target model | `cpnCycleClassData.Cohom _ := ℚ` even outside geometric nonzero degrees; restricted Hodge predicates do not prove equality with actual singular cohomology. |
| DeRham | 10 | Differential forms, exterior derivative, quotients, wedge and functorial helper results | `DeRhamIsomorphism` assumes the integration map is bijective; compatibility with geometric singular cohomology remains to construct. |
| Dolbeault | 3 | Complex differential/cohomology interfaces; conditional vanishing; closed zero-form components | Frozen build fails on namespace resolution in `DolbeaultTheorem`. Vanishing is a supplied hypothesis, not a proof for all contractible complex manifolds. |
| GAGA | 5 | Dimension/equivalence data and Hodge statement interfaces | F03 vacuous field; F04 clamped sum. `hodge_from_chain` assumes Hodge; `hodge_conjecture_for_class` consumes the full conjecture. |
| HardyLittlewood | 2 | Prime-pair definitions, count, row/tower requirements and infinitude consequences | `arbitrarily_large_pair` already asserts unbounded pairs. No Hardy–Littlewood asymptotic limit is encoded in `HardyLittlewoodRow`. |
| HodgeStar | 5 | Star/codifferential/Laplacian and pairing machinery | Track supplied finite-dimensional, inner-product, smoothness and adjointness structures. These do not automatically instantiate a compact manifold. |
| Kahler | 6 | Compatible J/inner products, operators, Hodge data, a separate sl2 injectivity argument | `HardLefschetzData` supplies injectivity/surjectivity; `LefschetzDecompositionData` supplies decomposition. Those fields are not unconditional geometric proofs. |
| Polignac | 1 | Statement definition and implications to twin/bounded gaps | Assumes infinitude of every positive even-gap row. |
| PrincipalBundles | 2 | Principal-action interfaces; abelian curvature `dA`, `A+dθ`, nonnegative integrand | Explicitly abelian; no nonabelian bracket term or full integral is supplied by `Connection.lean`. |
| QuantumYM | 4 | Compact product/Haar constructions, Wilson/Boltzmann estimates, bounded-operator transfer and compatible-level results | Uniform gap, spectral transfer and real/complex transport remain inputs. Exact-level/scalar-shift examples are not a constructed interacting continuum QFT. |
| SchurTest | 1 | Finite matrix weighted inequality | Does not by itself establish an infinite-dimensional unbounded operator/domain theorem. |
| SeibergWitten | 1 | Negative-form Clifford algebra, relations and group/submonoid definitions using Mathlib | No Seiberg–Witten moduli/PDE existence theorem is supplied by the filename. |
| Sobolev | 7 | Operators, finite-dimensional/Fredholm interfaces, harmonic projections and conditional decomposition | `HarmonicProjectionData.fredholm_decomp` supplies solvability; `hodge_decomp` constructs terms from it. Completion, compactness and analytic applicability remain explicit obligations. |
| Tao | 2 | Bounded-gap statement and requirement; implication from an infinite exact row | `infinitely_many_bounded_gaps` is a required field. This does not formalize the Maynard–Tao proof. |
| TwinPrimes | 2 | Standard infinitude proposition and requirement projection | The manifest contains `twin_primes : TwinPrimeStatement`; no closed witness is constructed here. |
| Root | 1 | Imports all 76 non-root modules | Explicitly says `Ramtastic_Vega.lean` is unreleased. |

## Assumptions are not custom axioms

A theorem `P → P` needs no special axiom but proves no unconditional `P`.
Likewise a structure with a field `proof : P` can be declared without proving
that any such structure exists. This is the precise reason a successful axiom
audit and a scientific/theorem-content audit answer different questions.

Not every `True` occurrence is a bug. In `ImageInHodge`, `True` deliberately
expresses all elements of a particular algebraic model having an allowed type.
The problematic sheaf field is different: an unrestricted disjunction with
`True` makes the claimed condition hold for every input. The lexical scan's six
`True` tokens therefore are not reported as six defects.

## Sources and novelty classifications

- Rotation identities: familiar trigonometric representation of a complex
  structure; **equivalent** mathematical content, with project-specific packaging.
- Clifford identities: **adjacent/reused** Mathlib mathematics. Compare the
  exact imported `CliffordAlgebra` definitions and square/orthogonality lemmas.
- Prime and BSD requirement projections: **interfaces to existing statements**;
  no novelty claim is established by a theorem name.
- Projective-space model: **algebraic surrogate** with selected expected relations;
  equivalence to genuine geometry remains unresolved.
- Spectral transfer: **conditional operator consequence**; actual continuum
  realization and problem-level novelty remain unresolved.
- EFMW/Hypernym scientific implications: **unassessed**; this repository contains
  neither the required empirical benchmarks nor a supplied product correctness bridge.

Primary comparison sources (retrieved 2026-10-16):

- https://lean-lang.org/doc/reference/latest/ValidatingProofs/
- https://lean-lang.org/doc/reference/latest/Axioms/
- https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/CliffordAlgebra/Basic.html
- https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf

Live documentation versions provide background; the actual build is governed
only by Ramtastic's frozen toolchain and manifest, not by current documentation.
