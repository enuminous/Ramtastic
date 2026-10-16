#!/usr/bin/env python3
"""Reproduce the static, exact-arithmetic, and selected Zoo adapter audit.

This program does not substitute for Lean. Run the separately supplied Lean
build/audit/probes as described in README.md. Python 3.10+, standard library only.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from collections import Counter
from fractions import Fraction as F

TARGET = '916ab476012852778edd9ca63aecf200a8e90ed1'
ZOO = '15dfb335424e77e1458cd77996f23d074dac0d88'
ENGINE = '6fbd8beddf442e7adb752ec30ae054a25857602b'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(out, name, obj):
    (out / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')


def strip_lean(text):
    """Remove nested comments and strings, preserving offsets and line numbers.

    This is a lexical inventory, not a Lean parser. Quoted identifiers remain
    visible; tactic macros and elaborated declarations require the kernel audit.
    """
    result = list(text)
    i, depth = 0, 0
    while i < len(text):
        start = i
        if text.startswith('/-', i):
            depth, i = 1, i + 2
            while i < len(text) and depth:
                if text.startswith('/-', i): depth, i = depth + 1, i + 2
                elif text.startswith('-/', i): depth, i = depth - 1, i + 2
                else: i += 1
        elif text.startswith('--', i):
            i = text.find('\n', i)
            if i < 0: i = len(text)
        elif text[i] == '"':
            i += 1
            while i < len(text):
                if text[i] == '\\': i += 2
                elif text[i] == '"': i += 1; break
                else: i += 1
        else:
            i += 1
            continue
        for j in range(start, min(i, len(text))):
            if text[j] != '\n': result[j] = ' '
    if depth: raise ValueError('Unterminated block comment')
    return ''.join(result)


def source_audit(repo, out):
    paths = git(repo, 'ls-tree', '-r', '--name-only', TARGET).decode().splitlines()
    manifest, modules, declarations, signals, structures = [], {}, [], [], []
    declaration = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe|partial)\s+)*(theorem|lemma|def|abbrev|structure|class|instance|axiom|opaque|inductive)\s+([^\s({:\[]+)', re.M)
    signal = re.compile(r'\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|elab|run_cmd)\b|debug\.skipKernelTC|\bTrue\b')
    for path in paths:
        data = git(repo, 'show', TARGET + ':' + path)
        manifest.append({'path': path, 'bytes': len(data), 'sha256': sha(data)})
        if not path.endswith('.lean') or path == 'lakefile.lean': continue
        text = data.decode()
        clean = strip_lean(text)
        name = path[:-5].replace('/', '.')
        imports = re.findall(r'^\s*import\s+([\w.]+)', clean, re.M)
        matches = list(declaration.finditer(clean))
        counts = Counter(m.group(1) for m in matches)
        modules[name] = {'path': path, 'lines': text.count('\n'), 'imports': imports,
                         'source_named_declarations': dict(counts)}
        for i, m in enumerate(matches):
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            block = clean[m.start():end].strip()
            depth, cut = 0, len(block)
            for j,ch in enumerate(block):
                if ch in '([{': depth += 1
                elif ch in ')]}': depth -= 1
                if depth == 0 and (block.startswith(':=',j) or re.match(r'\bwhere\b',block[j:])):
                    cut=j; break
            header = block[:cut].strip()
            entry = {'module': name, 'path': path, 'line': text.count('\n', 0, m.start())+1,
                     'kind': m.group(1), 'name': m.group(2), 'header': header}
            declarations.append(entry)
            if m.group(1) in ('structure', 'class'):
                structures.append({**entry, 'source_block_without_comments': block})
        for m in signal.finditer(clean):
            signals.append({'path': path, 'line': text.count('\n', 0, m.start())+1,
                            'token': m.group(), 'context': text.splitlines()[text.count('\n',0,m.start())].strip()})
    visited, missing = set(), set()
    def visit(name):
        if name in visited: return
        if name not in modules: missing.add(name); return
        visited.add(name)
        for dep in modules[name]['imports']:
            if dep == 'Ramtastic' or dep.startswith('Ramtastic.'): visit(dep)
    visit('Ramtastic')
    unreachable = sorted(set(modules) - visited)
    assert not unreachable and not missing, (unreachable, missing)
    counts = Counter(d['kind'] for d in declarations)
    summary = {'target_commit': TARGET, 'tracked_files': len(paths),
               'released_lean_modules': len(modules), 'reachable_from_root': len(visited),
               'unreachable_modules': unreachable, 'missing_project_imports': sorted(missing),
               'source_named_declaration_counts': dict(counts),
               'source_named_theorems_and_lemmas': counts['theorem']+counts['lemma'],
               'safety_tokens': dict(Counter(s['token'] for s in signals)),
               'interpretation': 'Lexical counts exclude generated declarations; True occurrences require semantic review. Not a kernel result.'}
    save(out, 'source-manifest.json', manifest)
    save(out, 'source-inventory.json', {'summary': summary, 'modules': modules,
                                      'declarations': declarations, 'signals': signals})
    save(out, 'structure-fields.json', structures)
    return summary


def multiply(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def transpose(a): return [list(row) for row in zip(*a)]
def negative(a): return [[-v for v in row] for row in a]
def ident(n): return [[F(int(i==j)) for j in range(n)] for i in range(n)]


def exact_witnesses(out):
    j = [[F(0),F(-2)],[F(1,2),F(0)]]
    assert multiply(j,j) == negative(ident(2))
    assert sum(v*v for v in [j[0][0],j[1][0]]) == F(1,4) != 1
    a = [[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]]
    b = [[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]]
    assert transpose(a)==negative(a) and transpose(b)==negative(b)
    assert multiply(a,a)==negative(ident(4)) and multiply(b,b)==negative(ident(4))
    ab = multiply(a,b)
    assert transpose(ab)==negative(ab) and transpose(ab)!=ab
    dims=[1,7]
    assert all((x==dims[0]) or True for x in dims) and dims[0]!=dims[1]
    h = lambda p,q: 1 if (p,q) in {(0,0),(0,2),(2,0),(2,2)} else 20 if (p,q)==(1,1) else 0
    clamped=sum(h(min(p,2),min(3-p,2)) for p in range(4))
    bounded=sum(h(p,3-p) for p in range(4) if p<=2 and 3-p<=2)
    assert clamped==2 and bounded==0
    witnesses = [
      {'finding':'F01','claim':'J squared equals minus identity forces Euclidean isometry',
       'control':{'J':[[0,-1],[1,0]]},'attack':{'J':[[0,-2],['1/2',0]]},
       'output':{'squared_length_before':'1','squared_length_after':'1/4','J_squared':'-I'},
       'criterion':'Same square-minus-identity property, unequal Euclidean squared lengths'},
      {'finding':'F02','claim':'A product of two skew-adjoint operators is automatically self-adjoint',
       'control':{'A':a,'B':a},'attack':{'A':a,'B':b},
       'output':{'AB':ab,'transpose_AB':transpose(ab),'both_square_to_minus_I':True},
       'criterion':'Both factors skew-adjoint; product differs from its transpose'},
      {'finding':'F03','claim':'StructureSheafWithHodge.hodge_symmetry_0q constrains the cohomology dimensions',
       'control':{'dimensions':[1,1]},'attack':{'dimensions':dims},
       'output':{'field_satisfied':True,'dimensions_equal':False},
       'criterion':'The field is satisfied via Or.inr True.intro for unequal dimensions'},
      {'finding':'F04','claim':'Clamping out-of-range Hodge indices implements the bounded diagonal sum',
       'control':{'hodge_numbers':[[0,0,0],[0,0,0],[0,0,0]]},
       'attack':{'hodge_numbers':[[h(p,q) for q in range(3)] for p in range(3)]},
       'output':{'dimension':2,'degree':3,'clamped_sum':clamped,'bounded_sum':bounded},
       'criterion':'A symmetric nonnegative fixture yields different sums; no geometric realization needed to refute formula identity'}]
    for w in witnesses:
        w['changed_keys'] = sum(w['control'][k]!=w['attack'][k] for k in w['control'])
        w['status'] = 'demonstrated'
        w['method'] = 'exact rational/integer arithmetic; independent implementation from Lean probes'
    save(out,'counterexamples.json',witnesses)
    return witnesses


MISSING = {
 'TORTOISE':'No prospective candidate/control forecasts or observed labels; a source audit has no Brier scores.',
 'CAT':'No matched full/ablated loss experiment; logical hypothesis inspection is not an ablation-loss measurement.',
 'BAT':'No matched candidate, conventional baseline and placebo losses.',
 'HEDGEHOG':'No development/heldout environments and outcome gains.',
 'CROCODILE':'No treated/control pre/post measurements or causal identification design.',
 'TURTLE':'No calibrated invariant score or three independent applicable evidence groups. Source review and its tests share one target.',
 'MAGPIE':'No calibrated coherence/support/provenance scores or groundedness history. Traceable citations alone do not supply these scores.',
 'WOLF':'No time-indexed channel measurements for an EMA.',
 'CHAMELEON':'No observed context distances, adaptation baseline, or within/between noise estimates.',
 'JELLYFISH':'No measured system-health network, stress gains or incoming harm.',
 'BEAVER':'No target repair or measured intervention/rollback experiment was authorized as part of the audit.',
 'MANTIS':'No calibrated time series of variance, autocorrelation and curvature z-scores.',
 'BISON':'No workload demand, capacity or queue observations.',
 'SALMON':'Import links are recorded, but no justified influence weights or mass interpretation is supplied.',
 'ORCA':'No acknowledged operational handoff with measured payload/ownership/dependency flags.',
 'MOLE':'No calibrated surface/latent health indicators or detection coverage.',
 'LYNX':'Literature comparison is qualitative; numeric novelty distance, rarity and replication scores are not measured.',
 'HORSE':'No workload, attention or fatigue observations.',
 'TERMITE':'No interacting-agent state snapshot or neighbor weights.',
 'PHOENIX':'No damaged/recovered system or recovery hold-window series.',
 'COBRA':'No measured goal/proxy divergence or intent evidence; mathematical defects imply no intent attribution.',
 'WHALE':'No long-term observed series and baseline.',
 'FALCON':'No event/hazard/alarm timing experiment.',
 'RHINO':'No matched baseline/post-shock performance measurement.',
 'BONOBO':'No agent utilities, fairness or cooperation observations.',
 'AXOLOTL':'No observed damage/adaptation outcomes, costs or invariant-retention measurement.',
 'BUTTERFLY':'No justified nonlinear dynamical layer or measured cascade inputs.'}


def zoo_audit(repo, zoo, engine, out, witnesses):
    assert git(zoo,'rev-parse','HEAD').decode().strip()==ZOO
    assert git(engine,'rev-parse','HEAD').decode().strip()==ENGINE
    # Fail if the executable or specifications have tracked working-tree edits.
    for p in (zoo,engine):
        subprocess.run(['git','-C',str(p),'diff','--exit-code','HEAD','--'],check=True,stdout=subprocess.DEVNULL)
    sys.path.insert(0,str(engine))
    from research_engine.kernels import evaluate, describe
    from research_engine.examples.cases import cases, fixture_bindings
    coverage=json.loads((zoo/'coverage.json').read_text())
    old=json.loads((engine/'research_engine/data/zoo-specifications.json').read_text())
    schemas=[{**r,'adapter':describe(r['name']),
              'current_lean_sha256':sha((zoo/(r['module']+'.lean')).read_bytes()),
              'engine_snapshot_lean_sha256':sha(old[r['module']+'.lean'].encode()),
              'engine_commit':ENGINE} for r in coverage]
    # Write schemas, inputs and criteria before computations.
    save(out,'operation-catalogue.json',schemas)
    supplied=cases()
    save(out,'conformance-inputs.json',supplied)
    save(out,'operation-criteria.json',{
      'conformance':'All 46 published selected adapters return; 90 frozen reference values match with rel_tol=abs_tol=1e-12. This is a port regression, not target evidence.',
      'WEASEL':'Retain the four independently reproduced exact witnesses with one changed fixture key, positive witness indicator and budget 1; no counterexample search claimed.',
      'ELEPHANT':'One current event identifies the frozen source commit and terminates at the recorded snapshot origin. Earlier git history is outside this shallow snapshot.',
      'CIRCUS':'Gate the claim that all documented semantics are established. Material demonstrated specification/prose failures force FAIL. No independent-source flag is invented.',
      'MONSTER':'Retrospective audit has no preregistered performance envelope; source procedure must return N/A.',
      'other_target_operations':'Do not manufacture missing observations. Record required inputs and blocked applicability.'})
    runs=[{'animal':name,'kind':'conformance_fixture_only','input':data,'output':evaluate(name,data)}
          for name,data in sorted(supplied.items())]
    assert len(runs)==46 and len({r['animal'] for r in runs})==46
    outputs={r['animal']:r['output'] for r in runs}
    fixtures=json.loads((engine/'research_engine/data/zoo-reference-fixtures.json').read_text())
    bindings=fixture_bindings()
    comparisons=[]
    for f in fixtures:
        animal,field=bindings[f['label']]
        value=outputs[animal]
        for key in field.split('.'): value=value[int(key)] if isinstance(value,list) else value[key]
        matched=math.isclose(value,f['expected'],rel_tol=1e-12,abs_tol=1e-12)
        assert matched,(f,value)
        comparisons.append({'label':f['label'],'actual':value,'expected':f['expected'],'matched':matched})
    save(out,'conformance-results.json',{'runs':runs,'reference_comparisons':comparisons})
    ts=int(git(repo,'show','-s','--format=%ct',TARGET))
    target_inputs={
      'WEASEL':{'findings':[{'changed_keys':w['changed_keys'],'severity':1,'cost':w['changed_keys'],'reproducibility':1} for w in witnesses],'budget':1},
      'ELEPHANT':{'events':[{'id':1,'time':ts,'status':'active','supersedes':None,
                            'provenance':'https://github.com/enuminous/Ramtastic/tree/'+TARGET}], 'start':1,'fuel':2}}
    save(out,'target-operation-inputs.json',{
      'inputs':target_inputs,'definitions':{
       'severity':'1 means an exact counterexample was reproduced, not an estimated real-world risk',
       'cost':'Number of changed fixture keys, not time/money',
       'reproducibility':'1 means this exact Python witness executed successfully',
       'WEASEL_index_order':[w['finding'] for w in witnesses],
       'ELEPHANT_origin':'Boundary of available pinned snapshot, not earliest historical origin'}})
    target_outputs={name:evaluate(name,data) for name,data in target_inputs.items()}
    assert len(target_outputs['WEASEL']['retained'])==4
    assert target_outputs['ELEPHANT']['termination']=='origin'
    save(out,'target-operation-results.json',target_outputs)
    rows=[]
    for r in schemas:
        name=r['name']
        ranked=name not in MISSING and name not in target_inputs
        reason=(f"Requires precomputed component columns in the published {name} feature order; no corresponding observed dataset or justified Ramtastic adapter exists."
                if ranked else MISSING.get(name,''))
        rows.append({'id':r['id'],'animal':name,'purpose_and_transformation':r['adapter']['implemented_scope'],
                     'required_inputs':r['adapter']['parameters'],'current_formal_scope':r['scope'],
                     'criterion':'See operation-criteria.json; conformance is separate from target evaluation.',
                     'conformance_execution':'computed','target_execution':'computed' if name in target_inputs else 'blocked_missing_inputs',
                     'evidence_status':'demonstrated' if name in target_inputs else 'unresolved',
                     'target_result':target_outputs.get(name), 'limitation':reason or (
                         'Filtering supplied witnesses is not discovery or proof search.' if name=='WEASEL' else
                         'One-snapshot provenance bookkeeping does not reconstruct the unavailable earlier history.')})
    save(out,'zoo-46-ledger.json',rows)
    with (out/'zoo-46-ledger.csv').open('w',newline='') as f:
        keys=['id','animal','purpose_and_transformation','conformance_execution','target_execution','evidence_status','limitation']
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        w.writerows({k:r[k] for k in keys} for r in rows)
    lines=['# Complete canonical 46-operation ledger','',
           '46 selected adapters executed on published conformance fixtures. Two use explicitly defined target inputs; 44 lack required target observations. No fixture output is evidence for Ramtastic mathematics.','',
           '| # | Animal | Fixed operation | Target disposition |','|---:|---|---|---|']
    for r in rows:
        lines.append(f"| {r['id']} | {r['animal']} | {r['purpose_and_transformation']} | {r['target_execution']}: {r['limitation']} |")
    (out/'ZOO-46.md').write_text('\n'.join(lines)+'\n')
    return {'canonical_animals':len(rows),'conformance_adapters_executed':len(runs),
            'numeric_reference_matches':len(comparisons),'target_adapters_computed':len(target_outputs),
            'target_adapters_blocked':len(rows)-len(target_outputs)}


def extension_audit(zoo,out):
    sources=json.loads((zoo/'extension-sources.json').read_text())
    circus={'animal':'CIRCUS','decision':'FAIL',
      'pipeline':[{'stage':s,'provenance_status':'documented'} for s in ['definition','data_selection','labels','scoring','validation']],
      'dependencies':[{'materiality':'material','feedback':False,'note':'Proof fields remain explicit assumptions; no empirical independence claimed.'}],
      'risks':[{'id':f,'materiality':'material','status':'present'} for f in ['F01','F02','F03','F04']],
      'independent_checks':[]}
    monster={'animal':'MONSTER','decision':'N/A',
      'preregistration':{'registered_before_outcomes':False,'protocol_id':'retrospective-source-audit'},
      'metric':{'tolerance':None},'baseline':{'matched':False},'conditions':[]}
    inputs={'CIRCUS':circus,'MONSTER':monster}
    save(out,'extension-target-inputs.json',inputs)
    results=[]
    for name,suffix in [('CIRCUS','/Circus'),('MONSTER','/Zoo-Monster')]:
        row=next(r for r in sources if r['repository'].endswith(suffix) and r['path'].endswith('.py'))
        raw=row['content'].encode()
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob_sha1']
        ns={'__name__':'audit_extension'}
        exec(compile(row['content'],row['path'],'exec'),ns)
        result=ns['decide'](inputs[name]); assert result==inputs[name]['decision']
        results.append({'extension':name,'execution':'computed','output':result,
                        'source':{k:row[k] for k in ['repository','commit','path','git_blob_sha1']},
                        'interpretation':'Declared report gate only; not independent evidence or a finding that Lean is inconsistent.'})
    for name,reason in [
      ('CHIMERA','No classical/quantum record-recovery event is being evaluated.'),
      ('WOODPECKER','No measured ablation losses, matched baseline or validation record.'),
      ('NIGHTINGALE','No fitted prediction function, effect estimates or bootstrap/support data; branch projection only is tested upstream.')]:
        results.append({'extension':name,'execution':'blocked_missing_inputs','evidence_status':'unresolved','reason':reason})
    save(out,'extension-ledger.json',results)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','zoo','engine','out'): p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    assert git(a.source,'rev-parse',TARGET).decode().strip()==TARGET
    static=source_audit(a.source,a.out)
    witnesses=exact_witnesses(a.out)
    zoo=zoo_audit(a.source,a.zoo,a.engine,a.out,witnesses)
    extension_audit(a.zoo,a.out)
    result={'target_commit':TARGET,'zoo_commit':ZOO,'engine_commit':ENGINE,
            'static':static,'zoo':zoo,'exact_counterexamples':len(witnesses),
            'lean_status':'See separately captured exact-toolchain CI evidence; this script does not execute Lean.'}
    save(a.out,'run-summary.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
