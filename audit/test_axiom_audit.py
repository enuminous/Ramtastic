"""Failure controls distinguish a real axiom audit from a vacuous scan."""
from pathlib import Path
import subprocess
import tempfile

source = Path("audit/StrictAudit.lean").read_text()
marker = "open Lean in\nrun_cmd do"
assert source.count(marker) == 1
cases = [
    ("public axiom", "axiom AuditProbe.probe : False", "AuditProbe.probe"),
    ("private axiom", "namespace AuditProbe\nprivate axiom probe : False\nend AuditProbe", "probe"),
    ("placeholder", "theorem AuditProbe.probe : False := by sorry", "sorryAx"),
    ("native proof", "theorem AuditProbe.probe : (1 : Nat) = 1 := by native_decide", "Lean.ofReduceBool"),
]
with tempfile.TemporaryDirectory(prefix="ramtastic-audit-", dir=".") as directory:
    probe = Path(directory) / "Probe.lean"
    for label, declaration, expected in cases:
        probe.write_text(source.replace(marker, declaration + "\n\n" + marker))
        result = subprocess.run(["lake", "env", "lean", str(probe)],
                                text=True, capture_output=True, timeout=120)
        output = result.stdout + result.stderr
        if result.returncode == 0 or "Unapproved axiom" not in output or expected not in output:
            raise SystemExit(f"Failed to reject {label} for expected reason:\n{output}")
        print(f"CONTROL_PASS {label}: rejected {expected}")
