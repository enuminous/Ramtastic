# Frozen Ramtastic Zoo audit plan

Target: `enuminous/Ramtastic@916ab476012852778edd9ca63aecf200a8e90ed1`.
Audit requested by enuminous on 2026-10-16. This is a retrospective source audit,
not a prospectively blinded experiment. Initial README/source inspection preceded
this plan; subsequent executions and counterexample checks are recorded separately.

Lean: `leanprover/lean4:v4.30.0-rc1`; Mathlib:
`8ec19128ad27190c2ec7c872d504be0a2877bd68`. Preserve all dependency pins.
Canonical operation source:
`enuminous/Monolithic-Zoo-Lean4@15dfb335424e77e1458cd77996f23d074dac0d88`:
46 historical animals and five separately tracked extension procedures.
Executable selected Python adapters:
`enuminous/EFMW_Post156_Zoo_Audit@6fbd8beddf442e7adb752ec30ae054a25857602b`.
The engine has an older specification snapshot: preserve and disclose that pin;
do not represent its numerical adapters as full current pipeline equivalence.

## Criteria fixed before execution

1. Rebuild every released Lean module at the target's exact toolchain and manifest.
   Pass only if the build exits zero and all released source modules are covered.
   A download/setup failure is an infrastructure block, not a mathematical refutation.
2. Traverse all compiled Ramtastic declarations (including private declarations),
   reject dependencies on axioms other than `propext`, `Classical.choice`, and
   `Quot.sound`, and test rejection of an unused public axiom, private axiom,
   `sorry`, and native proof reduction. Record unsafe declarations separately.
3. Inventory every source file, imports, named declarations and explicit proof
   fields. Static token scanning strips comments/strings and is not a kernel audit.
4. Separate conditional consequences, statement definitions, instantiated
   constructions, documented claims, and unreleased code. A conclusion supplied
   as a field/hypothesis is not an unconditional proof of that conclusion.
5. Attack the documented implication from a square-minus-identity generator to
   Euclidean norm preservation, and the claim that two skew-adjoint factors have
   a self-adjoint product without an additional commutation hypothesis. Exact
   rational counterexamples suffice to reject those unrestricted implications.
   They do not refute the actual conditional rotation group law.
6. Review all 46 fixed animal operations plus five extensions for applicability.
   Execute only with real, defined inputs or clearly labeled conformance fixtures.
   No invented time series, benchmark scores, independent evidence groups, or
   scientific adapters. Missing inputs remain unresolved/not applicable, not passes.
7. Compare central claims to primary mathematical sources. Distinguish familiar
   identities from new implementation work; do not infer novelty from a new name.
8. Publish a flat archive with reports, input/provenance manifests, scripts,
   counterexamples and execution evidence. Check unique root-only ZIP filenames,
   SHA256 integrity, reproducer behavior and source coverage before publication.

Evidence grades: demonstrated; supported but incomplete; hypothesis/postulate;
unresolved; rejected. Execution status is separate from evidence grade. Multiple
Zoo outputs based on one source/build are not independent confirmations.
No empirical validation of EFMW, Hypernym products, or unreleased proof-theory
claims is in scope without an explicit artifact and evaluation protocol.
