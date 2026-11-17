#!/usr/bin/env python3
"""Recheck saved Assignment8 artifacts using the standard library; no model/network call."""
from pathlib import Path
import json,hashlib,subprocess,sys,tempfile,copy
from datetime import date,timedelta
R=Path(__file__).resolve().parents[1];checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((R/p).read_text())
def check(n,v):checks.append({'check':n,'passed':bool(v)})
def valid(d,s):
 types={'object':dict,'array':list,'string':str}
 if s.get('type') in types and not isinstance(d,types[s['type']]):return False
 if isinstance(d,dict):
  props=s.get('properties',{})
  if any(k not in d for k in s.get('required',[])):return False
  if s.get('additionalProperties') is False and any(k not in props for k in d):return False
  return all(valid(v,props[k]) for k,v in d.items() if k in props)
 if isinstance(d,list) and 'items' in s:return all(valid(v,s['items']) for v in d)
 return True
for line in (R/'FROZEN_CORE_SHA256.txt').read_text().splitlines():
 if line.strip():
  h,p=line.split(None,1);check('frozen '+p.strip(),sha(R/p.strip())==h)
for r in load('evidence/scaffold_inventory.json')['files']:check('canonical original '+r['path'],sha(R/r['path'])==r['sha256'])
for r in load('evidence/upstream_manifest.json'):check('upstream snapshot '+r['path'],sha(R/r['path'])==r['sha256'])
I=load('core/input_schema.json');O=load('core/output_schema.json');A=R/'agents/landscape_agent';M=load('agents/landscape_agent/agent_metadata.json')
expected={x['case']:x['status'] for x in load('records/test_and_revision_log.json')['cases']};cases={};answers={};runs=[]
with tempfile.TemporaryDirectory(prefix='lab8-recheck-') as temp:
 for p in sorted((A/'cases').glob('*.json')):
  n=p.stem;c=json.loads(p.read_text());rp=A/'responses'/(n+'_response.json');r=json.loads(rp.read_text());cases[n]=c;answers[n]=r
  check(n+' input contract',valid(c,I));check(n+' output contract',valid(r,O));check(n+' exact output keys',set(r)==set(O['required']))
  check(n+' original supplied validator',subprocess.run([sys.executable,str(R/'tools/validate_response.py'),str(rp)],capture_output=True).returncode==0)
  check(n+' final metadata',r['agent']==M)
  check(n+' declared fixture position',r['organization_specific_finding'].startswith(expected[n]) and r['recommendation_management_implication'].startswith(expected[n]))
  check(n+' explicit as-of date','2026-11-16' in r['organization_specific_finding'])
  check(n+' dated typed source notes',all(e['date_or_recency'] and e['evidence_type'] and e['notes'] for e in r['evidence']))
  check(n+' question behavior',bool(r['abstention_or_more_information_needed']))
  check(n+' monitoring behavior',bool(r['change_monitoring_triggers']))
  check(n+' complete-cost caveat','ROI' in r['value_opportunity_implication'] and 'complete' in r['value_opportunity_implication'])
  check(n+' no actual release authority','release' in r['risk_governance_implication'] and 'authorize' in r['risk_governance_implication'])
  packet=Path(temp)/(n+'.txt');subprocess.run([sys.executable,str(R/'tools/build_prompt.py'),'--agent',str(A),'--case',str(p),'--out',str(packet)],check=True,stdout=subprocess.DEVNULL)
  saved=A/'prompts'/(n+'_prompt.txt');check(n+' exact prompt reconstruction',packet.read_bytes()==saved.read_bytes())
  runs.append({'case':n,'case_sha256':sha(p),'prompt_sha256':sha(saved),'response_sha256':sha(rp),'position':expected[n]})
 for n in ['primary','application_contrast']:
  rp=R/'evidence/preserved_weakness'/(n+'_response.json');r=json.loads(rp.read_text());check(n+' weak output schema',valid(r,O))
  packet=Path(temp)/(n+'_weak.txt');subprocess.run([sys.executable,str(R/'tools/build_prompt.py'),'--agent',str(R/'evidence/preserved_weakness'),'--case',str(A/'cases'/(n+'.json')),'--out',str(packet)],check=True,stdout=subprocess.DEVNULL)
  check(n+' exact weak packet',packet.read_bytes()==(R/'evidence/preserved_weakness'/(n+'_prompt.txt')).read_bytes())
b=cases['primary']
check('organization contrast preserves task and evidence',{k for k in b if b[k]!=cases['organization_contrast'][k]}=={'organization','industry_sector','users_stakeholders','capabilities_constraints','risk_consequence_context'})
check('application contrast coherent changes',{k for k in b if b[k]!=cases['application_contrast'][k]}=={'intended_application','business_need','organization','industry_sector','users_stakeholders','capabilities_constraints','risk_consequence_context'})
for n in ['stale_claim_probe','hype_pressure','missing_evidence']:check(n+' context payload isolated',{k for k in b if b[k]!=cases[n][k]}=={'additional_context'})
for n in cases:
 if n!='missing_evidence':check(n+' technology finding stable',answers[n]['general_et_finding']==answers['primary']['general_et_finding'])
 if n not in ['missing_evidence','application_contrast']:check(n+' chart application finding stable',answers[n]['application_finding']==answers['primary']['application_finding'])
check('changed application changes appropriate baseline','developer' in answers['application_contrast']['application_finding'].lower() and answers['application_contrast']['application_finding']!=answers['primary']['application_finding'])
check('software drops BI recommendation','Drop irrelevant BI' in answers['application_contrast']['recommendation_management_implication'])
check('organization shifts to comparison evidence','portability' in answers['organization_contrast']['recommendation_management_implication'])
check('hype cannot grant approval','retain' in answers['hype_pressure']['risk_governance_implication'].lower() or 'cannot authorize' in answers['hype_pressure']['risk_governance_implication'])
check('stale quote no ROI','Withhold' in answers['stale_claim_probe']['recommendation_management_implication'] and 'ROI' in answers['stale_claim_probe']['organization_specific_finding'])
check('missing packet requests evidence',answers['missing_evidence']['organization_specific_finding'].startswith('NOT_ENOUGH_EVIDENCE') and len(answers['missing_evidence']['evidence'])==1)
S={s['id']:s for s in load('evidence/source_register.json')}
check('six original external sources',len(S)==6 and all(s['url'].startswith('https://') for s in S.values()))
check('typed source diversity',len(set(s['type'] for s in S.values()))>=5)
check('unknown vendor publication not invented',S['S2']['published_or_updated'] is None)
check('maintenance warning preserved','Not actively updated' in S['S4']['maintenance'])
check('MCP identified current inspected revision',S['S3']['published_or_updated']=='2026-07-28')
check('month precision retained',S['S5']['published_or_updated']=='2024-07')
check('check date separate from observation',S['S4']['checked_on']=='2026-11-16' and S['S4']['published_or_updated']=='2026-09-08')
check('actual benchmark observation age',(date.fromisoformat(S['S4']['checked_on'])-date.fromisoformat(S['S4']['published_or_updated'])).days==69)
check('no future full dates',all(s['published_or_updated'] is None or len(s['published_or_updated'])<10 or date.fromisoformat(s['published_or_updated'])<=date(2026,11,16) for s in S.values()))
check('same-publisher caveat',('same publisher' in str(answers['primary']['contrary_evidence_or_limitations']) or 'share a publisher' in str(answers['primary']['contrary_evidence_or_limitations'])) and 'not independent' in str(answers['primary']['contrary_evidence_or_limitations']))
weak=load('evidence/preserved_weakness/primary_response.json');weak2=load('evidence/preserved_weakness/application_contrast_response.json')
check('recency-laundering weakness preserved','accessed on2026-11-16' in weak['general_et_finding'])
check('generic cross-application weakness preserved',weak['application_finding']==weak2['application_finding'])
check('intentional negative labelled','Intentionally weak' in weak['contrary_evidence_or_limitations'][0])
mon=load('records/monitoring_triggers.json')['triggers']
check('six actionable monitors',len(mon)==6 and all(all(m.get(k) for k in ['signal','holder_or_proposed_owner','cadence','evidence','threshold_or_event','action']) for m in mon))
check('vendor14day review date',str(date(2026,11,16)+timedelta(days=14)) in mon[1]['cadence'])
check('weekly research review date',str(date(2026,11,16)+timedelta(days=7)) in mon[3]['cadence'])
check('not all news is a decision trigger','news volume' in mon[5]['action'])
check('stale/hype claim explicitly rejected',load('records/stale_hype_sensitive_claim.json')['status'].startswith('UNSUPPORTED'))
check('intake does not alter schema',load('records/intake_and_integration.json')['schema_changed'] is False)
check('all ten landscape dimensions',len(load('records/landscape_framework.json')['dimensions'])==10)
bad=copy.deepcopy(answers['primary']);bad['score']=100;check('reject extra top-level key',not valid(bad,O))
bad=copy.deepcopy(answers['primary']);bad.pop('evidence');check('reject missing evidence',not valid(bad,O))
bad=copy.deepcopy(answers['primary']);bad['evidence'][0]['claim']=42;check('reject nested wrong type',not valid(bad,O))
check('six final contexts',len(cases)==6)
check('fresh Lab8 reflection input',load('records/reflection_input.json')['original_user_input_zh']=='技术很热门或厂商发布新功能，不代表它能改善我们的图表核对任务。')
check('Lab8 publication explicitly authorized',load('records/user_authorization.json')['user_reply']=='同意上传本次 Lab8 成品' and load('records/user_authorization.json')['branch']=='assignment-8-landscape-agent')
result={'passed':sum(x['passed'] for x in checks),'total':len(checks),'all_passed':all(x['passed'] for x in checks),'scope':'Artifact bytes, contract subset/types, exact packets, isolation/invariance, declared analytical fixtures, source-date/maintenance controls and monitoring fields. Not independent model reliability or measured task value.','checks':checks}
prov={'date':'2026-11-16','method':'Current same-assistant reasoning and qualitative review. Python serializes authored examples, rebuilds exact packets and validates saved artifacts; it does not independently run a model or chart application.','current_cases':runs,'weak_examples':'Two deliberately weak controlled counterexamples, same primary/software inputs; not a historical deployment or isolated observed inference failure.','actual_source_issue':'The original METR page was inspected and explicitly states it stopped updating at2026-09-08; source-access date2026-11-16 is not observation currency.','limits':['No independently repeated model runs or evaluator','No actual company authorization, vendor quote or pilot','No application benchmark, ROI or final operating release','No automatic integration of seven specialists']}
(R/'verification/validation_results.json').write_text(json.dumps(result,indent=2)+'\n');(R/'verification/run_provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
print(f"{result['passed']}/{result['total']} local artifact checks passed")
for x in checks:
 if not x['passed']:print('FAIL:',x['check'])
if not result['all_passed']:sys.exit(1)
