"""Apply the documented namespace and zero-form proof experiment.

Never updates the source pin. The published repository retains the original
source; this mutation belongs only to a disposable diagnostic checkout.
"""
from pathlib import Path
import subprocess
import sys

target='916ab476012852778edd9ca63aecf200a8e90ed1'
path=Path('Ramtastic/Dolbeault/DolbeaultTheorem.lean')
original=subprocess.check_output(['git','show',f'{target}:{path}'])
if path.read_bytes()!=original:
    raise SystemExit('Refusing to alter a non-frozen Dolbeault source')
needle=b'namespace Ramtastic.Dolbeault.DolbeaultTheorem\n'
assert original.count(needle)==1
changed=original.replace(needle,needle+b'\nopen Ramtastic.ComplexStructure\n')
old=b'  have hdf := hclosed x\n'
new=old+b'  have hform : (fun x => extDeriv f x) = 0 := funext hclosed\n'
assert changed.count(old)==1
changed=changed.replace(old,new)
assert changed.count(b'this, hdf, pullbackJ_zero')==2
changed=changed.replace(b'this, hdf, pullbackJ_zero',b'this, hform, pullbackJ_zero')
path.write_bytes(changed)
print('DIAGNOSTIC_ONLY: opened Ramtastic.ComplexStructure; supplied function-level zero equality to the two imaginary-component simp proofs. The theorem statement is unchanged.')
print('Original release build remains FAILED. Subsequent Lean results concern this explicitly modified checkout.')
