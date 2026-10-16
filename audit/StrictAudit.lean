import Lean
import Ramtastic

/-! All imported Ramtastic declarations, including private names. -/
open Lean in
run_cmd do
  let env ← getEnv
  let allowed : Array Name := #[``propext, ``Classical.choice, ``Quot.sound]
  let mut count := 0
  let mut theoremCount := 0
  let mut unsafeCount := 0
  for (name, info) in env.constants.toList do
    let isProject := match env.getModuleIdxFor? name with
      | some idx => (`Ramtastic).isPrefixOf env.header.moduleNames[idx.toNat]!
      | none => (`AuditProbe).isPrefixOf (privateToUserName name)
    if isProject then
      if info.isUnsafe then
        unsafeCount := unsafeCount + 1
        logInfo m!"UNSAFE_DECL {name}"
      else
        count := count + 1
        if info matches .thmInfo _ then
          theoremCount := theoremCount + 1
        let axioms ← collectAxioms name
        for ax in axioms do
          unless allowed.contains ax do
            throwError "Unapproved axiom {ax} used by {name}"
  if count == 0 then
    throwError "Audit matched no project declarations"
  logInfo m!"AXIOM_AUDIT_PASS safe={count} theorems={theoremCount} unsafe={unsafeCount}"

#print axioms Ramtastic.Bass.HingeRotation.rotate_add
#print axioms Ramtastic.GAGA.ChowToHodge.hodge_from_chain
#print axioms Ramtastic.TwinPrimes.Tower.twinPrimes
