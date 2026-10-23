"""Reject missing imports and incomplete roots before the diagnostic build."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PIN = "8ec19128ad27190c2ec7c872d504be0a2877bd68"


def check():
    files = sorted((ROOT / "Ramtastic").rglob("*.lean"))
    modules = {p.relative_to(ROOT).with_suffix("").as_posix().replace("/", ".") for p in files}
    def imports(path):
        return set(re.findall(r"^import\s+([\w.]+)", path.read_text(), re.M))
    actual = imports(ROOT / "Ramtastic.lean")
    if actual != modules:
        raise SystemExit(f"Incomplete root: missing={modules-actual}, extra={actual-modules}")
    for path in files + [ROOT / "Ramtastic.lean"]:
        for module in imports(path):
            if module.startswith("Ramtastic.") and module not in modules:
                raise SystemExit(f"Missing import {module} in {path.relative_to(ROOT)}")
    # Preserve the frozen release's mathematical files before the disclosed
    # diagnostic patch is applied. Later extensions are additional inputs.
    for entry in json.loads((ROOT / "source-manifest.json").read_text()):
        if entry["path"].startswith("Ramtastic/") and entry["path"].endswith(".lean"):
            path = ROOT / entry["path"]
            if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
                raise SystemExit("Frozen release source changed: " + entry["path"])
    restored = json.loads((ROOT / "provenance/ci-restoration-2026-10-23.json").read_text())
    if hashlib.sha256((ROOT / restored["source_path"]).read_bytes()).hexdigest() != restored["sha256"]:
        raise SystemExit("Restored Clifford module differs from its pinned source")
    if (ROOT / "lakefile.toml").exists():
        raise SystemExit("Ambiguous active Lake configuration")
    if f'@ "{PIN}"' not in (ROOT / "lakefile.lean").read_text():
        raise SystemExit("Lake dependency must use the immutable Mathlib commit")
    package = next(p for p in json.loads((ROOT / "lake-manifest.json").read_text())["packages"] if p["name"] == "mathlib")
    if package["rev"] != PIN or package["inputRev"] != PIN:
        raise SystemExit("Mathlib dependency and lock disagree")
    if (ROOT / "lean-toolchain").read_text().strip() != "leanprover/lean4:v4.30.0-rc1":
        raise SystemExit("Unexpected toolchain")
    print(f"SOURCE_COMPLETENESS_PASS: all {len(modules)} modules imported; original source and restoration digests verified")


if __name__ == "__main__":
    check()
