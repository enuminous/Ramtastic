#!/bin/bash
set -u
ROOT=$(cd "$(dirname "$0")" && pwd)
export ELAN_HOME="$ROOT/elan" PATH="$ROOT/bin:$ROOT/elan/bin:$PATH" XDG_CACHE_HOME="$ROOT/cache"
cd "$ROOT/run/Ramtastic"
lake exe cache get Ramtastic > ../results/mathlib-cache-targeted.log 2>&1
s=$?; echo "cache_exit=$s"; [ "$s" = 0 ] || exit "$s"
lake build > ../results/frozen-build.log 2>&1
s=$?; echo "original_build_exit=$s"
[ "$s" != 0 ] && grep -q 'DelDelBar.del' ../results/frozen-build.log || exit 99
mkdir audit
cp "$ROOT"/audit/{StrictAudit.lean,ReleasedSubsetAudit.lean,SemanticProbes.lean,test_axiom_audit.py,diagnostic_namespace.py} audit/
set -e
lake env lean -DwarningAsError=true audit/ReleasedSubsetAudit.lean > ../results/released-subset-audit.log 2>&1
python3 audit/test_axiom_audit.py audit/ReleasedSubsetAudit.lean > ../results/axiom-controls.log 2>&1
python3 audit/diagnostic_namespace.py > ../results/diagnostic-patch.log 2>&1
git diff > ../results/diagnostic.patch
lake build > ../results/diagnostic-build.log 2>&1
lake env lean -DwarningAsError=true audit/StrictAudit.lean > ../results/axiom-audit.log 2>&1
lake env lean -DwarningAsError=true audit/SemanticProbes.lean > ../results/semantic-probes.log 2>&1
git diff --exit-code -- lean-toolchain lakefile.lean lake-manifest.json
printf 'REPRODUCTION_PASS\n'
