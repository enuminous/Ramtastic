#!/usr/bin/env python3
"""Build the offline index and deterministic flat ZIP from this audit directory."""
import hashlib
import html
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent
NAME='Ramtastic-Zoo-Audit-2026-10-16.zip'


def main():
    rows=json.loads((ROOT/'zoo-46-ledger.json').read_text())
    summary=json.loads((ROOT/'run-summary.json').read_text())
    evidence=json.loads((ROOT/'execution-evidence.json').read_text())
    if evidence.get('publication_ready') is not True:
        raise SystemExit('Refusing to package unfinished execution evidence.')
    esc=html.escape
    table=''.join(f"<tr data-state='{r['target_execution']}'><td>{r['id']}</td><td><b>{esc(r['animal'])}</b></td><td>{esc(r['purpose_and_transformation'])}</td><td>{esc(r['target_execution'].replace('_',' '))}</td><td>{esc(r['limitation'])}</td></tr>" for r in rows)
    diagnostic=esc(evidence['diagnostic_result'])
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ramtastic · Monolithic Zoo audit</title><style>
:root{color-scheme:light;--ink:#152b37;--teal:#006d70;--paper:#f4f7f7;--line:#cfdbde}
*{box-sizing:border-box}body{font:16px/1.6 system-ui,sans-serif;color:var(--ink);background:var(--paper);margin:0}
main{max-width:1200px;margin:auto;padding:44px 24px}h1{font-size:clamp(30px,5vw,48px);line-height:1.12;margin:12px 0}h2{margin-top:38px;font-size:25px}a{color:var(--teal)}.eyebrow{letter-spacing:.12em;font-size:12px;font-weight:750;text-transform:uppercase}.intro{max-width:850px;font-size:19px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin:28px 0}.card{background:white;border:1px solid var(--line);border-radius:10px;padding:18px}.number{display:block;font-size:32px;font-weight:750;color:var(--teal)}.note{background:#fff4df;border-left:4px solid #ac6413;padding:16px 20px}.links{display:flex;flex-wrap:wrap;gap:12px 24px}.tools{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0}input,select{font:inherit;border:1px solid #a6b8be;border-radius:5px;padding:10px;background:white}input{flex:1;min-width:220px}.scroll{overflow:auto;border:1px solid var(--line);border-radius:8px;background:white}table{border-collapse:collapse;width:100%;min-width:850px;font-size:14px}th,td{text-align:left;padding:12px;border-bottom:1px solid var(--line);vertical-align:top}th{background:#e5eeee;position:sticky;top:0}td:nth-child(2){white-space:nowrap}code{font-family:ui-monospace,monospace;font-size:.9em}footer{margin:36px 0;color:#4a626b;font-size:13px}
</style><main><div class="eyebrow">eNuminous · EFMW / Monolithic Zoo · 16 October 2026</div>
<h1>Ramtastic: what the formalization establishes</h1>
<p class="intro">A reproducible audit of the released Lean source, its mathematical interfaces, and its documentation. Four exact witnesses distinguish valid conditional mathematics from missing assumptions and incorrect specifications.</p>
<div class="cards"><div class="card"><span class="number">77</span>released Lean modules inventoried</div><div class="card"><span class="number">46</span>fixed Zoo operations reviewed</div><div class="card"><span class="number">90 / 90</span>numeric conformance comparisons</div><div class="card"><span class="number">4</span>exact adversarial witnesses</div></div>
<div class="note"><b>Frozen release build: failed.</b> Dolbeault namespace resolution fails at the original commit. Diagnostic result: '''+diagnostic+'''. A diagnostic success applies to an explicitly modified checkout. Original mathematical files remain preserved in the published fork.</div>
<h2>Read the evidence</h2><nav class="links"><a href="REPORT.md">Complete report</a><a href="VERIFICATION.md">Build and axiom evidence</a><a href="SOURCE-REVIEW.md">Mathematical scope</a><a href="counterexamples.json">Exact witnesses</a><a href="SemanticProbes.lean">Lean probes</a><a href="README.md">Reproduce the audit</a><a href="SHA256SUMS.txt">File checksums</a></nav>
<h2>Four precise findings</h2><ul><li><b>Inner-product boundary:</b> J² = −I alone does not force Euclidean norm preservation. This does not refute a theorem that separately assumes skew-adjointness.</li><li><b>Incorrect unrestricted shortcut:</b> two skew-adjoint factors need not have a self-adjoint product.</li><li><b>Vacuous field:</b> a sheaf “symmetry” condition ends in “or True”.</li><li><b>Incorrect sum:</b> clamped Hodge indices add out-of-range entries to a diagonal sum.</li></ul>
<h2>Every canonical animal</h2><p>All 46 selected adapters ran on published conformance fixtures. Only WEASEL and ELEPHANT had explicitly defined target inputs. The other 44 remain blocked by missing observations or mappings. No fixture result is promoted to mathematical or scientific evidence.</p>
<div class="tools"><input id="query" type="search" aria-label="Search animals and operations" placeholder="Search animals, operations, or missing inputs"><select id="state" aria-label="Filter target execution"><option value="all">All target dispositions</option><option value="computed">Computed target inputs</option><option value="blocked_missing_inputs">Missing target inputs</option></select></div><p id="count" aria-live="polite">46 animals shown</p><div class="scroll"><table><thead><tr><th>#</th><th>Animal</th><th>Fixed operation</th><th>Target execution</th><th>Limit / missing input</th></tr></thead><tbody>'''+table+'''</tbody></table></div>
<p><a href="zoo-46-ledger.json">Machine-readable ledger</a> · <a href="zoo-46-ledger.csv">CSV</a> · <a href="operation-catalogue.json">Input schemas and source pins</a> · <a href="extension-ledger.json">Five separately tracked extensions</a></p>
<h2>What remains open</h2><p>Concrete geometric/arithmetic instances, corrected Hodge specifications, a clean release build, and the exact unpublished halting theorem. No claim about EFMW physics or Hypernym product performance was tested here.</p>
<footer>Original Ramtastic attribution: C. Forrester (Adauriel), with per-file formalization credits. Audit prepared with AI assistance for Matthew Chenoweth Wright / eNuminous. Target: <code>916ab476012852778edd9ca63aecf200a8e90ed1</code>. This page works offline and makes no network requests.</footer></main>
<script>const q=document.getElementById('query'),s=document.getElementById('state'),rows=[...document.querySelectorAll('tbody tr')];function filter(){let n=0;for(const r of rows){const show=r.textContent.toLowerCase().includes(q.value.toLowerCase())&&(s.value==='all'||r.dataset.state===s.value);r.hidden=!show;if(show)n++;}document.getElementById('count').textContent=n+' animals shown';}q.addEventListener('input',filter);s.addEventListener('change',filter);</script></html>'''
    (ROOT/'index.html').write_text(page)
    files=sorted(p for p in ROOT.iterdir() if p.is_file() and p.name not in
                 {NAME,NAME+'.sha256','SHA256SUMS.txt','PACKAGE-MANIFEST.json'} and p.suffix not in {'.zip','.sha256'})
    assert len({p.name for p in files})==len(files)
    manifest={'archive':NAME,'layout':'flat; all files at archive root',
              'target_commit':summary['target_commit'],'files':[p.name for p in files],
              'excluded':'Original project dependency tree and binaries; fetch exact pins with reproduce.py.'}
    (ROOT/'PACKAGE-MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    files.append(ROOT/'PACKAGE-MANIFEST.json');files.sort()
    sums=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in files)
    (ROOT/'SHA256SUMS.txt').write_text(sums);files.append(ROOT/'SHA256SUMS.txt')
    dest=ROOT/NAME
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files):
            info=zipfile.ZipInfo(p.name,(2026,10,16,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(dest) as z:
        assert z.testzip() is None
        assert all('/' not in x and '\\' not in x for x in z.namelist())
        assert len(z.namelist())==len(set(z.namelist()))
    digest=hashlib.sha256(dest.read_bytes()).hexdigest()
    (ROOT/(NAME+'.sha256')).write_text(digest+'  '+NAME+'\n')
    print(json.dumps({'archive':str(dest),'files':len(files),'bytes':dest.stat().st_size,'sha256':digest,'flat':True}))


if __name__=='__main__':main()
