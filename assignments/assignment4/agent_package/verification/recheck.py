"""Recheck saved artifacts; does not call a model or certify reasoning quality."""
from pathlib import Path
import json,hashlib,subprocess,sys,copy
P=Path(__file__).resolve().parents[1];A=P/'agents/promethean_classification_agent';checks=[]
def read(p):return json.loads(p.read_text())
def check(name,ok,detail=''):checks.append(dict(check=name,passed=bool(ok),detail=detail))
def errors(x,s,loc='$'):
 supported={'$schema','title','type','required','properties','items','additionalProperties'}
 if set(s)-supported:return [loc+': unsupported schema keyword']
 types={'object':dict,'array':list,'string':str}
 if not isinstance(x,types.get(s.get('type'),type(None))):return [loc+': wrong type']
 out=[]
 if isinstance(x,dict):
  out += [loc+': missing '+k for k in s.get('required',[]) if k not in x]
  if s.get('additionalProperties') is False:out += [loc+': extra '+k for k in x if k not in s.get('properties',{})]
  for k,sub in s.get('properties',{}).items():
   if k in x:out+=errors(x[k],sub,loc+'.'+k)
 if isinstance(x,list):
  for i,y in enumerate(x):out+=errors(y,s['items'],f'{loc}[{i}]')
 return out
out=read(P/'core/output_schema.json');inp=read(P/'core/input_schema.json')
proc=subprocess.run([sys.executable,str(P/'tools/check_frozen_core.py')],capture_output=True,text=True)
check('seven frozen files intact',proc.returncode==0,proc.stdout.strip())
cases={p.stem:read(p) for p in (A/'cases').glob('*.json')};responses={}
for name,c in sorted(cases.items()):
 check(name+' input schema',not errors(c,inp),str(errors(c,inp)))
 r=read(A/'responses'/f'{name}_response.json');responses[name]=r
 check(name+' full output schema',not errors(r,out),str(errors(r,out)))
 proc=subprocess.run([sys.executable,str(P/'tools/validate_response.py'),str(A/'responses'/f'{name}_response.json')],capture_output=True,text=True)
 check(name+' instructor validator',proc.returncode==0,proc.stdout.strip())
 check(name+' current metadata',r['agent']==read(A/'agent_metadata.json'))
 check(name+' analytical question',r['analytical_question']==c['management_question'])
 prompt=(A/'prompts'/f'{name}_prompt.txt').read_text()
 check(name+' prompt case and frozen instructions',json.dumps(c,indent=2) in prompt and (P/'core/common_instructions.md').read_text() in prompt)
 check(name+' evidence IDs and dates',all(s in json.dumps(r['evidence']) for s in ['S0','S1','S2','S3','S4','S5','S6','2026-10-19']))
fixed=['emerging_technology','intended_application','business_need','management_question','time_horizon','additional_context']
check('matched context contrast holds shared fields fixed',all(cases['primary'][k]==cases['contrast'][k] for k in fixed))
changed=[k for k in cases['primary'] if cases['primary'][k]!=cases['posture_probe'][k]]
check('posture probe changes one field',changed==['adoption_posture'],str(changed))
check('stable general finding across organization and posture',responses['primary']['general_et_finding']==responses['contrast']['general_et_finding']==responses['posture_probe']['general_et_finding'],'Intentional reuse is a fixture, not statistical reliability.')
check('context implications differ',responses['primary']['organization_specific_finding']!=responses['contrast']['organization_specific_finding'])
check('component gate stops scoring',responses['component_probe']['general_et_finding'].startswith('Gate 1 STOP:'))
check('hype challenge and denominator distinction','generation-only' in responses['hype_probe']['organization_specific_finding'] and 'Reject' in responses['hype_probe']['organization_specific_finding'])
check('posture does not create permissions','cannot create a permitted environment' in responses['posture_probe']['organization_specific_finding'])
for c in ['primary','contrast','hype_probe','posture_probe']:
 check(c+' six criterion coverage',all(x in responses[c]['general_et_finding'] for x in ['C1','C2','C3','C4','C5','C6']))
check('support and contrary case retained',all('Strongest higher-significance' in responses[c]['contrary_evidence_or_limitations'][0] for c in responses))
baseline=read(A/'revisions/v0_1/hype_overclaim_response.json')
check('diagnostic baseline conforms structurally',not errors(baseline,out),'Structural validity does not endorse its deliberately unsupported claims.')
bp=(A/'revisions/v0_1/hype_prompt.txt').read_text()
check('unchanged hype input in diagnostic and final packets',json.dumps(cases['hype_probe'],indent=2) in bp)
check('baseline authorship disclosed','deliberately' in (A/'revisions/v0_1/specialist_instructions.md').read_text() and 'intentionally' in (P/'records/test_and_revision_log.md').read_text())
check('reflection authorship disclosed',read(P/'records/reflection_provenance.json')['student_personal_input_supplied'] is False)
for label,change in [('missing required',lambda r:r.pop('general_et_finding')),('extra key',lambda r:r.update(extra='not allowed')),('nested type',lambda r:r['evidence'][0].update(notes=7))]:
 r=copy.deepcopy(responses['primary']);change(r);check('negative control '+label,bool(errors(r,out)))
lineage=read(P/'evidence/prior_lab_lineage.json')
check('prior case snapshots unchanged',all(hashlib.sha256((P/x['retained_path']).read_bytes()).hexdigest()==x['sha256'] for x in lineage))
sources=read(P/'evidence/source_register.json')
check('dated source register and limits',len(sources)==7 and all(x.get('checked_on')=='2026-10-19' and x.get('limits') for x in sources))
inputs=read(P/'evidence/input_integrity.json');available=[x for x in inputs if Path(x['path']).exists()]
check('available original course inputs unchanged',all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in available),f'{len(available)}/{len(inputs)} sources available; OS metadata excluded.')
result={'passed':sum(x['passed'] for x in checks),'failed':sum(not x['passed'] for x in checks),'checks':checks,'scope':'Saved-artifact schema, source-integrity and explicit fixture checks; not model accuracy, verified student learning, human source review or a rubric score.'}
(P/'verification/validation_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
for x in checks:
 if not x['passed']:print('FAILED',x)
sys.exit(bool(result['failed']))
