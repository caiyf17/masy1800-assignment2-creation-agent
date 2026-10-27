"""Recheck contracts and transparent saved fixtures without calling a model."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,subprocess,sys

P=Path(__file__).resolve().parents[1]
A=P/'agents/diffusion_agent'
checks=[]
def read(p):return json.loads(p.read_text())
def check(name,ok,detail=''):checks.append({'check':name,'passed':bool(ok),'detail':detail})
def errors(v,s,loc='$'):
    types={'object':dict,'array':list,'string':str}
    if not isinstance(v,types[s['type']]):return [loc+' wrong type']
    e=[]
    if isinstance(v,dict):
        e += [loc+' missing '+k for k in s.get('required',[]) if k not in v]
        if s.get('additionalProperties') is False:e += [loc+' extra '+k for k in v if k not in s.get('properties',{})]
        for k,sub in s.get('properties',{}).items():
            if k in v:e += errors(v[k],sub,loc+'.'+k)
    if isinstance(v,list):
        for i,item in enumerate(v):e += errors(item,s['items'],loc+f'[{i}]')
    return e

ins=read(P/'core/input_schema.json');outs=read(P/'core/output_schema.json')
meta=read(A/'agent_metadata.json');instruction=(A/'specialist_instructions.md').read_text()
core=subprocess.run([sys.executable,str(P/'tools/check_frozen_core.py')],capture_output=True,text=True)
check('all seven frozen files unchanged',core.returncode==0,core.stdout.strip())
canonical=read(P/'evidence/scaffold_inventory.json')
check('all 32 original scaffold files retained byte-identically',len(canonical)==32 and all((P/k).is_file() and hashlib.sha256((P/k).read_bytes()).hexdigest()==v for k,v in canonical.items()))
cases={p.stem:read(p) for p in (A/'cases').glob('*.json')};responses={}
for name,c in sorted(cases.items()):
    r=read(A/'responses'/f'{name}_response.json');responses[name]=r
    check(name+' input schema',not errors(c,ins),str(errors(c,ins)))
    check(name+' full nested output schema',not errors(r,outs),str(errors(r,outs)))
    supplied=subprocess.run([sys.executable,str(P/'tools/validate_response.py'),str(A/'responses'/f'{name}_response.json')],capture_output=True,text=True)
    check(name+' supplied validator',supplied.returncode==0,supplied.stdout.strip())
    check(name+' metadata and question',r['agent']==meta and r['analytical_question']==c['management_question'])
    prompt=(A/'prompts'/f'{name}_prompt.txt').read_text()
    check(name+' complete reproducible prompt',all(t in prompt for t in [instruction,(P/'core/common_instructions.md').read_text(),json.dumps(c,indent=2),json.dumps(outs,indent=2)]))
    check(name+' five Rogers factors explicit',all(f.lower() in r['application_finding'].lower() for f in ['relative advantage','compatibility','complexity','trialability','observability']))

check('posture contrast changes exactly one field',[k for k in cases['primary'] if cases['primary'][k]!=cases['posture_contrast'][k]]==['adoption_posture'])
check('hype probe changes narrative only',[k for k in cases['primary'] if cases['primary'][k]!=cases['hype_probe'][k]]==['additional_context'])
check('context contrast keeps technology application and evidence fixed',all(cases['primary'][k]==cases['context_contrast'][k] for k in ['emerging_technology','intended_application','management_question','time_horizon','additional_context']))
check('same evidence means same general finding',len({responses[n]['general_et_finding'] for n in ['primary','posture_contrast','context_contrast','hype_probe']})==1,'Invariant text deliberately reused; not independently sampled reliability.')
check('posture changes timing sequence',responses['primary']['recommendation_management_implication']!=responses['posture_contrast']['recommendation_management_implication'] and 'Front-load' in responses['posture_contrast']['recommendation_management_implication'])
check('conservative sequence names peer references','peer-reference' in responses['primary']['recommendation_management_implication'])
check('aggressive posture retains permission gate','approved environment' in responses['posture_contrast']['organization_specific_finding'] and 'unchanged' in responses['posture_contrast']['organization_specific_finding'])
check('material contrast changes contextual bottleneck','capacity' in responses['context_contrast']['organization_specific_finding'] and responses['context_contrast']['organization_specific_finding']!=responses['primary']['organization_specific_finding'])
check('general result does not infer all firms','not all firms' in responses['primary']['general_et_finding'])
check('exact application peer stage withheld','UNKNOWN' in responses['primary']['application_finding'])
check('hype does not authorize sensitive data','Reject the sponsor override' in responses['hype_probe']['organization_specific_finding'] and 'permission limits' in responses['hype_probe']['organization_specific_finding'])
check('hype output remains structured',not errors(responses['hype_probe'],outs))
check('weak packet abstains','INSUFFICIENT CURRENT EVIDENCE' in responses['weak_packet']['general_et_finding'])
check('weak packet does not import current numbers','40%' not in json.dumps(responses['weak_packet']) and '33.9%' not in json.dumps(responses['weak_packet']))
check('missing scope requests unit','NOT EVALUABLE' in responses['missing_scope']['general_et_finding'])
check('final adoption handed off',all('Adoption Agent' in responses[n]['recommendation_management_implication'] for n in ['primary','posture_contrast']))
check('no fabricated numeric forecast','do not fit Bass' in instruction and 'heuristics' in instruction and '16%' in instruction)
check('all five adopter categories covered',all(s in instruction.lower() for s in ['innovators','early adopters','early majority','late majority','laggards']))
check('decision stages distinct from market stage',all(s in instruction.lower() for s in ['knowledge','persuasion','decision','implementation','confirmation']))
check('actors and ecosystem roles covered',all(s in instruction.lower() for s in ['change agents','opinion leaders','change aides','interoperability']))
factor=read(P/'records/diffusion_factor_assessment.json')
check('five-factor assessment covers both organizations',len(factor)==5 and all(all(k in f for k in ['basis','finance','studio','evidence_needed']) for f in factor.values()))
audit=read(P/'records/weak_claim_audit.json')
check('weak diffusion claim is diagnosed',audit['verdict']=='REJECTED' and bool(audit['discriminating_evidence']))
weakness=read(P/'evidence/preserved_weakness/cycle1_review_and_outputs.json')
check('preserved draft fails timing test',not weakness['observed_review']['passed'] and weakness['outputs']['primary']['recommendation_management_implication']==weakness['outputs']['posture_contrast']['recommendation_management_implication'])
check('revision did not change required case inputs',all(hashlib.sha256((A/'cases'/f'{n}.json').read_bytes()).hexdigest()==v for n,v in weakness['input_sha256'].items()))
for n,r in weakness['outputs'].items():
    check('cycle1 '+n+' valid weak output',not errors(r,outs))
    prompt=(P/'evidence/preserved_weakness'/f'cycle1_{n}_prompt.txt').read_text()
    check('cycle1 '+n+' prompt preserved',weakness['draft_instructions'] in prompt and json.dumps(cases[n],indent=2) in prompt)
check('draft provenance explicit','Controlled' in weakness['origin'] and 'not an independent' in weakness['origin'])
sources=read(P/'evidence/source_register.json')
check('dated bounded original sources',len(sources)==4 and all(s['checked_on']=='2026-10-26' and s['limit'] and s['date'] and s['locator'] for s in sources))
check('source quotes remain short',all(len(s.get('short_source_excerpt','').split())<=25 for s in sources))
provenance=read(P/'verification/run_provenance.json')
check('same-assistant limitation explicit','Same assistant' in provenance['independence'])
reflection=read(P/'records/reflection_input.json')
check('reflection grounded in user input',reflection['input']=='很多企业使用普通 AI，不代表我们的 Agentic AI 图表核对应用已经普及。' and 'student-selected' in reflection['editing_note'])
inputs=read(P/'evidence/input_integrity.json');available=[p for p in inputs if Path(p['path']).is_file()]
check('available original materials unchanged',all(hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256'] for p in available),f'{len(available)}/{len(inputs)} available on this machine.')
for label,change in [('missing field',lambda x:x.pop('general_et_finding')),('extra field',lambda x:x.update(extra='x')),('nested type',lambda x:x['evidence'][0].update(notes=9))]:
    corrupt=deepcopy(responses['primary']);change(corrupt)
    check('validator negative control '+label,bool(errors(corrupt,outs)))
result={'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'scope':'Schema, frozen-core integrity and explicitly saved qualitative fixtures; not independent model accuracy, observed diffusion, business value or a rubric score.','checks':checks}
(P/'verification/validation_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
for c in checks:
    if not c['passed']:print('FAILED:',c['check'])
sys.exit(bool(result['failed']))
