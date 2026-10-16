"""Apply only the documented one-line namespace experiment to the frozen file.

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
path.write_bytes(changed)
print('DIAGNOSTIC_ONLY: opened Ramtastic.ComplexStructure; no theorem statement or proof text changed.')
print('Original release build remains FAILED. Subsequent Lean results concern this explicitly modified checkout.')
