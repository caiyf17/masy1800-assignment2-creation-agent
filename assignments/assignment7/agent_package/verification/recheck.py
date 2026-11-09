#!/usr/bin/env python3
"""Recheck saved Lab7 artifacts with the standard library; no model is invoked."""
from pathlib import Path
import json,hashlib,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(rel):return json.loads((ROOT/rel).read_text())
def check(name,value):checks.append({'check':name,'passed':bool(value)})
def valid(d,s):
 types={'object':dict,'array':list,'string':str}
 if s.get('type') in types and not isinstance(d,types[s['type']]):return False
 if isinstance(d,dict):
  p=s.get('properties',{})
  if any(k not in d for k in s.get('required',[])):return False
  if s.get('additionalProperties') is False and any(k not in p for k in d):return False
  return all(valid(v,p[k]) for k,v in d.items() if k in p)
 if isinstance(d,list) and 'items' in s:return all(valid(x,s['items']) for x in d)
 return True
for line in (ROOT/'FROZEN_CORE_SHA256.txt').read_text().splitlines():
 if line.strip():
  expected,rel=line.split(None,1);check('frozen '+rel.strip(),sha(ROOT/rel.strip())==expected)
for row in load('evidence/scaffold_inventory.json')['files']:check('canonical original '+row['path'],sha(ROOT/row['path'])==row['sha256'])
for row in load('evidence/upstream_manifest.json'):check('unchanged upstream '+row['snapshot'],sha(ROOT/row['snapshot'])==row['sha256'])
meta=load('agents/organizational_adoption_agent/agent_metadata.json');intake=load('core/input_schema.json');output=load('core/output_schema.json')
framework=load('records/readiness_framework.json');domains=[r['id'] for r in framework['domains']];profiles=load('records/readiness_profiles.json')
expected={r['case']:r['judgment'] for r in load('records/decision_table.json')};cases={};responses={};runs=[]
with tempfile.TemporaryDirectory(prefix='lab7-recheck-') as temp:
 for p in sorted((ROOT/'agents/organizational_adoption_agent/cases').glob('*.json')):
  name=p.stem;case=json.loads(p.read_text());cases[name]=case
  response=ROOT/'agents/organizational_adoption_agent/responses'/f'{name}_response.json';r=json.loads(response.read_text());responses[name]=r
  check(name+' common intake contract',valid(case,intake));check(name+' common output contract',valid(r,output))
  check(name+' original supplied validator',subprocess.run([sys.executable,str(ROOT/'tools/validate_response.py'),str(response)],capture_output=True).returncode==0)
  check(name+' final metadata',r['agent']==meta)
  check(name+' declared readiness judgment',r['recommendation_management_implication'].split(' — ',1)[0]==expected[name])
  check(name+' all eight domains in profile',[x['id'] for x in profiles[name]['domains']]==domains)
  check(name+' all eight domains in response',all(d in r['organization_specific_finding'] for d in domains))
  check(name+' explicit evidence states',all(d['status'] in framework['evidence_states'] for d in profiles[name]['domains']))
  check(name+' missing-information behavior',bool(r['abstention_or_more_information_needed']))
  check(name+' general finding invariant',r['general_et_finding']==load('agents/organizational_adoption_agent/responses/primary_response.json')['general_et_finding'])
  check(name+' application finding invariant',r['application_finding']==load('agents/organizational_adoption_agent/responses/primary_response.json')['application_finding'])
  check(name+' dated limited evidence',all(e['date_or_recency'] and e['notes'] for e in r['evidence']))
  rebuilt=Path(temp)/(name+'.txt')
  subprocess.run([sys.executable,str(ROOT/'tools/build_prompt.py'),'--agent','agents/organizational_adoption_agent','--case',str(p),'--out',str(rebuilt)],capture_output=True,check=True)
  prompt=ROOT/'agents/organizational_adoption_agent/prompts'/f'{name}_prompt.txt'
  check(name+' exact prompt reconstruction',rebuilt.read_bytes()==prompt.read_bytes())
  runs.append({'case':name,'case_sha256':sha(p),'prompt_sha256':sha(prompt),'response_sha256':sha(response),'judgment':expected[name]})
 for name in ['primary','readiness_contrast']:
  response=ROOT/'evidence/preserved_weakness'/f'{name}_v0.1.json';weak=json.loads(response.read_text())
  check(name+' controlled weak format valid',valid(weak,output))
  rebuilt=Path(temp)/(name+'_weak.txt')
  subprocess.run([sys.executable,str(ROOT/'tools/build_prompt.py'),'--agent',str(ROOT/'evidence/preserved_weakness'),'--case',str(ROOT/'agents/organizational_adoption_agent/cases'/f'{name}.json'),'--out',str(rebuilt)],capture_output=True,check=True)
  check(name+' controlled weak exact prompt',rebuilt.read_bytes()==(ROOT/'evidence/preserved_weakness'/f'{name}_v0.1_prompt.txt').read_bytes())
def diff(a,b):return [k for k in a if a[k]!=b[k]]
base=cases['primary']
for name in ['readiness_contrast','sponsor_only','bounded_poc_only','capacity_unknown','capacity_shortfall','ownership_loss']:
 check(name+' changes only capabilities_constraints',diff(base,cases[name])==['capabilities_constraints'])
check('hype appends context only',diff(base,cases['hype_probe'])==['additional_context'])
check('primary and materially improved profile change readiness',expected['primary']=='NOT_READY_FOR_DEFINED_SCOPE' and expected['readiness_contrast']=='SUPPORTED_CONDITIONAL_ON_ADOPTION_CLEARANCE')
check('critical unknown distinct from known gap',expected['capacity_unknown']=='MORE_EVIDENCE_REQUIRED' and expected['capacity_shortfall']=='NOT_READY_FOR_DEFINED_SCOPE')
check('sponsorship cannot average away blocker',expected['sponsor_only']==expected['primary'])
check('learning permission not operating readiness',expected['bounded_poc_only']=='LIMITED_LEARNING_ONLY' and 'No internal data' in responses['bounded_poc_only']['recommendation_management_implication'])
check('loss of owner reverses readiness',expected['ownership_loss']=='NOT_READY_FOR_DEFINED_SCOPE' and 'sponsor inherited' in responses['ownership_loss']['recommendation_management_implication'])
check('untrusted enthusiasm does not promote readiness',expected['hype_probe']==expected['primary'])
check('unsafe memo request declined','Decline its request' in responses['hype_probe']['recommendation_management_implication'])
check('baseline analyst experience not invented training','not provided' in profiles['primary']['domains'][1]['evidence'])
check('baseline culture acceptance not invented',profiles['primary']['domains'][6]['status']=='UNKNOWN')
check('primary critical external route gap',profiles['primary']['domains'][3]['status']=='GAP_IN_CASE')
check('prioritized primary proposed roles','P0:' in responses['primary']['recommendation_management_implication'] and 'roles are proposals' in responses['primary']['recommendation_management_implication'])
check('conditional support not launch permission','Do not launch' in responses['readiness_contrast']['recommendation_management_implication'])
unknown=responses['capacity_unknown']['organization_specific_finding']+' '+responses['capacity_unknown']['recommendation_management_implication']
check('unknown capacity has no imported numeric demand',all(x not in unknown for x in ['120','1440','1,440','24 planned','32 protected']))
check('unknown requests protected hours and cover','protected hours' in responses['capacity_unknown']['recommendation_management_implication'] and 'cover' in responses['capacity_unknown']['recommendation_management_implication'])
capacity={'status':'Fictional planning arithmetic, not measured workload or productivity','charts_per_week':120,'complete_review_minutes_per_chart':12,'demand_minutes_per_week':120*12,'demand_hours_per_week':120*12/60,'R1_protected_hours':2*16,'shortfall_profile_protected_hours':2*6,'shortfall_hours':120*12/60-2*6,'no_buffer_ceiling_charts':2*6*60/12}
check('capacity arithmetic with units',capacity['demand_hours_per_week']==24 and capacity['shortfall_hours']==12 and capacity['no_buffer_ceiling_charts']==60)
check('no-buffer maximum not operating recommendation','not a safe authorized target' in responses['capacity_shortfall']['recommendation_management_implication'])
weak=load('evidence/preserved_weakness/primary_v0.1.json');check('weak maturity conflation retained','technology itself is immature' in weak['general_et_finding'])
check('weak missing-information flaw retained','fill the missing' in weak['abstention_or_more_information_needed'][0])
check('eight dimensions, no arbitrary total',len(domains)==8 and 'No weighted average' in framework['decision_rule'])
check('three dependency priorities',[r['priority'] for r in load('records/prioritized_actions.json')]==['P0','P1','P2'])
check('use case and PoC handoff exists','not an implemented chart tool' in (ROOT/'records/poc_and_use_case.md').read_text())
check('future intake maps to existing contract',len(load('records/intake_requirements.json'))==10)
check('actual reflection input preserved',load('records/reflection_input.json')['user_input_zh']=='准备度不足不等于技术不成熟，应先找出可以补齐的组织缺口，而不是直接否定技术。')
check('publication explicitly authorized',load('records/user_authorization.json')['user_reply']=='同意上传本次 Lab7 成品')
check('eight final cases',len(cases)==8)
provenance={'date':'2026-11-09','runtime':'Current ChatGPT/Codex assistant; no separate inference API','method':'The assistant reasoned through and authored qualitative examples. Scripts serialize responses, reconstruct prompts and validate saved artifacts. Declared judgments are analytical fixtures, not an independent benchmark oracle.','limits':['No isolated model repeats or independent evaluator','Controlled weak baseline explicitly distinguishes deliberate diagnostic examples from an actual packaging-name issue','R1/L1 and capacity inputs are fictional; no firm permission, charter, training, budget or chart trial actually obtained','No actual ROI, current model qualification, technology maturity change or compliance certification claimed'],'instructions_sha256':sha(ROOT/'agents/organizational_adoption_agent/specialist_instructions.md'),'metadata_sha256':sha(ROOT/'agents/organizational_adoption_agent/agent_metadata.json'),'cases':runs}
for rel,data in [('verification/capacity_check.json',capacity),('verification/run_provenance.json',provenance)]:
 (ROOT/rel).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
result={'passed':sum(c['passed'] for c in checks),'total':len(checks),'all_passed':all(c['passed'] for c in checks),'scope':'Byte integrity, frozen schema keywords, exact packet reconstruction, case isolation, declared readiness/profile constraints, attribution and arithmetic; not future LLM reliability','checks':checks}
(ROOT/'verification/validation_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(f"{result['passed']}/{result['total']} local artifact checks passed")
for c in checks:
 if not c['passed']:print('FAIL:',c['check'])
if not result['all_passed']:sys.exit(1)
