#!/usr/bin/env python3
"""Verify the flat bundle, then reproduce pinned Python/optional Lean observations."""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys

HERE=Path(__file__).resolve().parent
PINS={
 'Ramtastic':'916ab476012852778edd9ca63aecf200a8e90ed1',
 'Monolithic-Zoo-Lean4':'15dfb335424e77e1458cd77996f23d074dac0d88',
 'EFMW_Post156_Zoo_Audit':'6fbd8beddf442e7adb752ec30ae054a25857602b'}


def verify():
    manifest=HERE/'SHA256SUMS.txt'
    if not manifest.exists():
        raise SystemExit('Run from the extracted flat ZIP, which includes SHA256SUMS.txt.')
    count=0
    for line in manifest.read_text().splitlines():
        digest,name=line.split('  ',1)
        if Path(name).name!=name: raise SystemExit('Non-flat manifest path')
        path=HERE/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise SystemExit('Integrity mismatch: '+name)
        count+=1
    print(f'INTEGRITY_PASS {count} files')


def run(args,cwd,log=None,expected=0):
    if log:
        with log.open('w') as f:
            r=subprocess.run(args,cwd=cwd,text=True,stdout=f,stderr=subprocess.STDOUT)
    else: r=subprocess.run(args,cwd=cwd)
    if expected is not None and r.returncode!=expected:
        raise SystemExit(f'Unexpected exit {r.returncode}: {args}; inspect {log}')
    return r.returncode


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verify-only',action='store_true')
    p.add_argument('--work-dir',type=Path)
    p.add_argument('--lean',action='store_true')
    a=p.parse_args(); verify()
    if a.verify_only:return
    if a.work_dir is None:p.error('--work-dir is required unless --verify-only')
    work=a.work_dir.resolve()
    if work.exists():raise SystemExit('Choose a new work directory; refusing to overwrite '+str(work))
    work.mkdir(parents=True)
    results=work/'results';results.mkdir()
    for name,commit in PINS.items():
        dest=work/name;dest.mkdir()
        run(['git','init','--quiet'],dest)
        run(['git','remote','add','origin','https://github.com/enuminous/'+name+'.git'],dest)
        run(['git','fetch','--depth','1','origin',commit],dest,results/(name+'-fetch.log'))
        run(['git','checkout','--detach',commit],dest,results/(name+'-checkout.log'))
    source=work/'Ramtastic';zoo=work/'Monolithic-Zoo-Lean4';engine=work/'EFMW_Post156_Zoo_Audit'
    run([sys.executable,str(HERE/'run_audit.py'),'--source',str(source),'--zoo',str(zoo),
         '--engine',str(engine),'--out',str(results)],work,results/'python-run.log')
    for generated in results.glob('*.json'):
        shipped=HERE/generated.name
        if shipped.exists() and shipped.read_bytes()!=generated.read_bytes():
            raise SystemExit('Reproduction differs: '+generated.name)
    run([sys.executable,'-m','unittest','discover','-s','research_engine/tests','-v'],engine,results/'engine-tests.log')
    for script in ['verify.py','scripts/extension_fixtures.py','scripts/report_fixtures.py','scripts/threshold_fixtures.py']:
        run([sys.executable,script],zoo,results/(Path(script).stem+'.log'))
    if a.lean:
        run(['lake','exe','cache','get'],source,results/'mathlib-cache.log')
        status=run(['lake','build'],source,results/'frozen-build.log',expected=None)
        text=(results/'frozen-build.log').read_text()
        if status==0 or 'Unknown identifier' not in text or 'DelDelBar.del' not in text:
            raise SystemExit('Original namespace failure was not reproduced; inspect frozen-build.log')
        audit=source/'audit';audit.mkdir()
        for f in ['StrictAudit.lean','ReleasedSubsetAudit.lean','SemanticProbes.lean','test_axiom_audit.py','diagnostic_namespace.py']:
            shutil.copy2(HERE/f,audit/f)
        run(['lake','env','lean','-DwarningAsError=true','audit/ReleasedSubsetAudit.lean'],source,results/'released-subset-audit.log')
        run([sys.executable,'audit/test_axiom_audit.py','audit/ReleasedSubsetAudit.lean'],source,results/'axiom-controls.log')
        run([sys.executable,'audit/diagnostic_namespace.py'],source,results/'diagnostic-patch.log')
        run(['lake','build'],source,results/'diagnostic-build.log')
        run(['lake','env','lean','-DwarningAsError=true','audit/StrictAudit.lean'],source,results/'axiom-audit.log')
        run(['lake','env','lean','-DwarningAsError=true','audit/SemanticProbes.lean'],source,results/'semantic-probes.log')
        run(['git','diff','--exit-code','--','lean-toolchain','lakefile.lean','lake-manifest.json'],source)
    print('REPRODUCTION_PASS; results in',results)
    if a.lean:print('Frozen release: FAILED as recorded. Namespace/zero-form diagnostic: passed. These are distinct results.')


if __name__=='__main__':main()
