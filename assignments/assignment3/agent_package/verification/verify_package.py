#!/usr/bin/env python3
"""Saved-artifact checks using only the standard library; not a model benchmark."""
from pathlib import Path
import json,hashlib,subprocess,sys,copy,tempfile
ROOT=Path(__file__).resolve().parents[1]
AG=ROOT/'agents/innovation_disruption_agent'
checks=[]
def read(p):return json.loads(p.read_text())
def check(label,ok,detail):checks.append({'check':label,'passed':bool(ok),'detail':detail})
def errors(value,schema,path='$'):
    ts={'object':dict,'array':list,'string':str}
    typ=schema.get('type')
    if typ in ts and not isinstance(value,ts[typ]):return [path+': wrong type']
    result=[]
    if typ=='object':
        for k in schema.get('required',[]):
            if k not in value:result.append(path+': missing '+k)
        props=schema.get('properties',{})
        if schema.get('additionalProperties') is False:
            result.extend(path+': extra '+k for k in value if k not in props)
        for k,s in props.items():
            if k in value:result.extend(errors(value[k],s,path+'.'+k))
    if typ=='array':
        for i,v in enumerate(value):result.extend(errors(v,schema['items'],path+f'[{i}]'))
    return result
def course(p):return subprocess.run([sys.executable,str(ROOT/'tools/validate_response.py'),str(p)],capture_output=True,text=True)
core=subprocess.run([sys.executable,str(ROOT/'tools/check_frozen_core.py')],capture_output=True,text=True)
check('Frozen core integrity',core.returncode==0,core.stdout.strip()+core.stderr.strip())
out_schema=read(ROOT/'core/output_schema.json'); in_schema=read(ROOT/'core/input_schema.json'); meta=read(AG/'agent_metadata.json')
rs={}; cs={}
for name in ('primary','contrast','borderline'):
    cs[name]=c=read(AG/'cases'/f'{name}.json');rs[name]=r=read(AG/'responses'/f'{name}_response.json')
    check(name+' input contract',not errors(c,in_schema),errors(c,in_schema))
    check(name+' full output contract',not errors(r,out_schema),errors(r,out_schema))
    cr=course(AG/'responses'/f'{name}_response.json');check(name+' course validator',cr.returncode==0,cr.stdout.strip())
    check(name+' version',r['agent']==meta,'Metadata matches submitted agent')
    check(name+' source references',all(s['url'] in ' '.join(e['source_or_reference'] for e in r['evidence']) for s in read(ROOT/'evidence/source_register.json')),'References exist; source applicability was reviewed separately')
    check(name+' prompt packet',(AG/'prompts'/f'{name}.txt').is_file() and (AG/'specialist_instructions.md').read_text() in (AG/'prompts'/f'{name}.txt').read_text(),'Packet contains final specialist logic')
    check(name+' fictional context','Fictional analytical scenario' in c['additional_context'],'Organization assumptions identified')
    check(name+' role boundary',all(x in r['recommendation_management_implication'] for x in ('Adoption','Readiness','Diffusion','Promethean','Landscape')),'Routes consequential adjacent questions')
check('Shared contrast conditions',all(cs['primary'][k]==cs['contrast'][k] for k in ('emerging_technology','management_question','time_horizon')),'Technology, question and horizon fixed; other variables change together')
check('Appropriately stable general finding',len({r['general_et_finding'] for r in rs.values()})==1,'Intentionally reused general analysis, not independent repeatability')
check('Context-sensitive business-model contrast','Judgment: Low' in rs['primary']['organization_specific_finding'] and 'Judgment: Moderate' in rs['contrast']['organization_specific_finding'],'Different positions in the value chain explain qualitative contrast')
check('Conditional alternative preserved','remain Low' in rs['contrast']['contrary_evidence_or_limitations'][0],'Media efficiency-only interpretation is not suppressed')
check('Borderline challenges branding','does not demonstrate' in rs['borderline']['application_finding'],'Fixed automation is not accepted as adaptive tool use')
check('Missing business model abstention','Judgment: Withheld' in rs['borderline']['organization_specific_finding'] and len(rs['borderline']['abstention_or_more_information_needed'])>=3,'Withholds unsupported disruption level and requests relevant inputs')
check('Implementation distinction',all('propos' in r['application_finding'].lower() and 'implement' in r['application_finding'].lower() for r in rs.values()),'Proposed and implemented status differentiated')
rev=read(AG/'records/revision_evidence.json')
check('Saved diagnostic contract',not errors(rev['baseline_response'],out_schema),'An analytically weak example can be structurally valid')
check('Failure and correction trace',len(rev['diagnosis'])>=3 and len(rev['revision'])>=3 and rev['corrected_primary'].endswith('primary_response.json'),'Novelty, implementation and disruption defects recorded')
with tempfile.TemporaryDirectory(prefix='lab3-invalid-json-') as td:
    v=copy.deepcopy(rs['primary']);v['unsupported_extra']=True
    check('Reject extra output field',bool(errors(v,out_schema)),'Frozen output disallows unrecognized top-level fields')
    v=copy.deepcopy(rs['primary']);del v['general_et_finding'];p=Path(td)/'missing.json';p.write_text(json.dumps(v))
    check('Reject missing finding',course(p).returncode!=0 and bool(errors(v,out_schema)),'Both the frozen validator and complete contract check reject missing field')
result={'date':'2026-10-12','scope':'Saved artifacts, schema and targeted regression checks; does not measure live model reliability or business outcomes','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks}
(ROOT/'verification/validation_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f"{result['passed']}/{result['total']} checks passed")
for c in checks:
    if not c['passed']:print('FAILED',c)
sys.exit(0 if all(c['passed'] for c in checks) else 1)
