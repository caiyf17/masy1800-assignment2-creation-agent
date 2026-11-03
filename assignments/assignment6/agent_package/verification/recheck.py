#!/usr/bin/env python3
"""Validate saved Lab6 examples and package integrity without invoking a model."""
from pathlib import Path
import json,hashlib,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parents[1]
checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(rel):return json.loads((ROOT/rel).read_text())
def check(name,value):checks.append({'check':name,'passed':bool(value)})
def valid(data,schema):
    """Validate the keywords used in the frozen contracts, not arbitrary JSON Schema."""
    types={'object':dict,'array':list,'string':str}
    if schema.get('type') in types and not isinstance(data,types[schema['type']]):return False
    if isinstance(data,dict):
        props=schema.get('properties',{})
        if any(k not in data for k in schema.get('required',[])):return False
        if schema.get('additionalProperties') is False and any(k not in props for k in data):return False
        return all(valid(v,props[k]) for k,v in data.items() if k in props)
    if isinstance(data,list) and 'items' in schema:return all(valid(v,schema['items']) for v in data)
    return True
for line in (ROOT/'FROZEN_CORE_SHA256.txt').read_text().splitlines():
    if line.strip():
        expected,rel=line.split(None,1);check('frozen '+rel,sha(ROOT/rel.strip())==expected)
for row in load('evidence/scaffold_inventory.json')['files']:
    check('original scaffold '+row['path'],sha(ROOT/row['path'])==row['sha256'])
for row in load('evidence/upstream_manifest.json'):
    check('upstream bytes '+row['snapshot'],sha(ROOT/row['snapshot'])==row['sha256'])
meta=load('agents/adoption_agent/agent_metadata.json');intake=load('core/input_schema.json');output=load('core/output_schema.json')
cases={};responses={};run=[]
expected={d['case']:d['primary_action'] for d in load('records/decision_table.json')}
with tempfile.TemporaryDirectory(prefix='lab6-recheck-') as temporary:
    for p in sorted((ROOT/'agents/adoption_agent/cases').glob('*.json')):
        name=p.stem;case=json.loads(p.read_text());cases[name]=case
        response_path=ROOT/'agents/adoption_agent/responses'/f'{name}_response.json'
        r=json.loads(response_path.read_text());responses[name]=r
        check(name+' intake contract',valid(case,intake))
        check(name+' strict output contract',valid(r,output))
        result=subprocess.run([sys.executable,str(ROOT/'tools/validate_response.py'),str(response_path)],capture_output=True,text=True)
        check(name+' supplied response validator',result.returncode==0)
        check(name+' current agent metadata',r['agent']==meta)
        action=r['recommendation_management_implication'].split(' — ',1)[0]
        check(name+' declared primary action',action==expected[name])
        check(name+' organizational specialist boundary','Organizational Adoption' in r['recommendation_management_implication'])
        rebuilt=Path(temporary)/(name+'.txt')
        subprocess.run([sys.executable,str(ROOT/'tools/build_prompt.py'),'--agent','agents/adoption_agent','--case',str(p),'--out',str(rebuilt)],capture_output=True,check=True)
        prompt=ROOT/'agents/adoption_agent/prompts'/f'{name}_prompt.txt'
        check(name+' exact prompt reconstruction',rebuilt.read_bytes()==prompt.read_bytes())
        check(name+' general evidence invariant',r['general_et_finding']==load('agents/adoption_agent/responses/primary_response.json')['general_et_finding'])
        check(name+' source dates and limits',all(e['date_or_recency'] and e['notes'] for e in r['evidence']))
        run.append({'case':name,'case_sha256':sha(p),'prompt_sha256':sha(prompt),'response_sha256':sha(response_path),'action':action})

a=cases['primary'];b=cases['posture_contrast']
check('posture changes only adoption_posture',[k for k in a if a[k]!=b[k]]==['adoption_posture'])
for field in ['general_et_finding','evidence','confidence_and_uncertainty','risk_governance_implication']:
    check('posture invariant '+field,responses['primary'][field]==responses['posture_contrast'][field])
check('posture action meaningfully changes',expected['primary']=='MONITOR' and expected['posture_contrast']=='PROOF_OF_CONCEPT')
check('posture permissions identical',a['capabilities_constraints']==b['capabilities_constraints'])
c=cases['permission_blocked']
check('permission contrast changes only constraint',[k for k in b if b[k]!=c[k]]==['capabilities_constraints'])
check('permission veto despite aggressive posture',expected['permission_blocked']=='DEFER' and c['adoption_posture']==b['adoption_posture'])
check('permission response names prerequisite','written permitted environment' in responses['permission_blocked']['recommendation_management_implication'])
check('missing application is empty',cases['missing_application']['intended_application']=='')
check('missing scope explicit abstention','withheld' in responses['missing_application']['application_finding'] and expected['missing_application']=='DEFER')
check('hype appends only untrusted context',[k for k in a if a[k]!=cases['hype_probe'][k]]==['additional_context'])
check('hype does not promote action',expected['hype_probe']==expected['primary'])
check('unsafe memo rejected','unsafe upload' in responses['hype_probe']['recommendation_management_implication'])
check('positive H1 not routine implementation',expected['qualified_experiment']=='BOUNDED_EXPERIMENT' and 'not routine implementation' in responses['qualified_experiment']['application_finding'])
check('positive H2 case evidence replaces baseline','unvalidated application' not in responses['staged_adoption']['application_finding'] and 'replace baseline unknowns' in responses['staged_adoption']['application_finding'])
check('positive H2 consumes separate readiness','separate readiness assessment' in responses['staged_adoption']['application_finding'])
check('positive H2 scope remains one team','one reporting team only' in responses['staged_adoption']['recommendation_management_implication'])
check('no zero-risk claim','not proof of zero risk' in responses['staged_adoption']['application_finding'])
check('all six categories exercised',set(expected.values())=={'ADOPT','BOUNDED_EXPERIMENT','PROOF_OF_CONCEPT','MONITOR','DEFER','REJECT_FOR_PRESENT'})
check('primary active review date','21 days' in responses['primary']['recommendation_management_implication'])
check('PoC time effort cap','eight analyst-hours over two weeks' in responses['posture_contrast']['recommendation_management_implication'])
check('PoC no internal-data scope','No production integration, internal data' in responses['posture_contrast']['recommendation_management_implication'])
check('H1 experiment scope and cap','two analysts and a 16-hour cap' in responses['qualified_experiment']['recommendation_management_implication'])

comparison={'status':'Hypothetical H3 effort proxy, not actual performance or monetary ROI','reviews_per_month':100,'manual_minutes':100*30,'deterministic_minutes':100*20,'agent_minutes':100*(3+12+7)+300,'separate_past_sunk_minutes_excluded':300}
comparison['agent_disadvantage_vs_best_minutes']=comparison['agent_minutes']-min(comparison['manual_minutes'],comparison['deterministic_minutes'])
check('H3 full effort arithmetic',comparison['agent_minutes']==2500 and comparison['agent_disadvantage_vs_best_minutes']==500)
check('H3 best comparator, not only manual','best adequate baseline' in responses['inferior_alternative']['application_finding'])
check('H3 monetary ROI not invented','financial prices and ROI are unknown' in responses['inferior_alternative']['application_finding'])
(ROOT/'verification/effort_comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')

weak=[]
for p in sorted((ROOT/'evidence/preserved_weakness').glob('*.json')):
    d=json.loads(p.read_text());check('preserved format-valid weakness '+p.name,valid(d,output));weak.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p)})
check('actual context-leakage draft retained','unvalidated application' in load('evidence/preserved_weakness/staged_adoption_before_scope_revision.json')['application_finding'])
check('controlled baseline permission flaw retained','typical internal reporting charts' in load('evidence/preserved_weakness/primary_response_v0.1.json')['recommendation_management_implication'])
check('reflection has actual user input',load('records/reflection_input.json')['user_input_zh']=='即使很多同行采用，也要比较人工或简单工具，确认新增价值和完整成本。')
check('publication explicitly authorized',load('records/user_authorization.json')['user_reply']=='同意上传本次 Lab6 成品')
check('eight final cases',len(cases)==8)
provenance={'date':'2026-11-02','runtime':'Current ChatGPT/Codex assistant session; no independent model API call','method':'The assistant authored and reviewed qualitative examples. Local scripts serialize text, build prompts and validate saved artifacts. Expected actions are declared analytical fixtures, not a benchmark oracle.','limits':['No independent evaluator or isolated repeats','No chart tool, company trial, regulatory certification or actual permission obtained','H1-H3 are fictional branch controls; K0 is an explicit new Lab6 teaching premise','Observed prior outputs, controlled negative examples and actual working-draft leakage revision are separately identified'],'instructions_sha256':sha(ROOT/'agents/adoption_agent/specialist_instructions.md'),'metadata_sha256':sha(ROOT/'agents/adoption_agent/agent_metadata.json'),'cases':run,'preserved_weaknesses':weak}
(ROOT/'verification/run_provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
result={'passed':sum(c['passed'] for c in checks),'total':len(checks),'all_passed':all(c['passed'] for c in checks),'scope':'Byte integrity, frozen contract keywords, reproducible prompt construction, declared action/invariance and arithmetic checks; not measured model reliability','checks':checks}
(ROOT/'verification/validation_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f"{result['passed']}/{result['total']} local checks passed")
for c in checks:
    if not c['passed']:print('FAIL',c['check'])
sys.exit(0 if result['all_passed'] else 1)
