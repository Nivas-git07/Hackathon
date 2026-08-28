from __future__ import annotations

import csv, io, json
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from math import sin


def series():
    result=[]; start=date(2026,1,5)
    for week in range(30):
        day=start+timedelta(days=week*7); production=1000+week*4+42*sin(week/2.2)
        baseline=94+2.2*sin(week/2.8)+(week%3)*.35; counter=baseline+(.8 if week>=13 else 0); actual=baseline
        if week>=13: actual=counter*.897; production*=1.085
        result.append({'date':day.isoformat(),'actual':round(actual,1),'counterfactual':round(counter,1) if week>=13 else None,'predicted':round(counter*.86,1) if week>=13 else None,'lower':round(counter*.973,1) if week>=13 else None,'upper':round(counter*1.027,1) if week>=13 else None,'production':round(production)})
    return result


FACILITIES=[
 {'id':'chennai','name':'Chennai Assembly Plant','type':'Assembly','city':'Chennai','readiness':92},
 {'id':'hosur','name':'Hosur Manufacturing Plant','type':'Manufacturing','city':'Hosur','readiness':84},
 {'id':'bengaluru','name':'Bengaluru Distribution Centre','type':'Distribution','city':'Bengaluru','readiness':76}]
INTERVENTIONS=[
 {'id':'hvac','name':'HVAC scheduling optimisation','facility':'Chennai Assembly Plant','category':'HVAC','predicted':14.0,'cost_lakh':2.4,'co2_reduction_t':164,'downtime_days':1,'risk':'Low','evidence':88,'status':'Pilot ready'},
 {'id':'compressed-air','name':'Compressed air leak programme','facility':'Hosur Manufacturing Plant','category':'Process energy','predicted':11.0,'cost_lakh':4.8,'co2_reduction_t':128,'downtime_days':2,'risk':'Low','evidence':81,'status':'Candidate'},
 {'id':'led','name':'LED loading-zone retrofit','facility':'Bengaluru Distribution Centre','category':'Lighting','predicted':21.0,'cost_lakh':16.0,'co2_reduction_t':76,'downtime_days':2,'risk':'Low','evidence':91,'status':'Verified'},
 {'id':'solar','name':'Rooftop solar phase II','facility':'Hosur Manufacturing Plant','category':'Renewable energy','predicted':25.0,'cost_lakh':38.0,'co2_reduction_t':390,'downtime_days':5,'risk':'Medium','evidence':79,'status':'Candidate'},
 {'id':'motors','name':'High-efficiency motor retrofit','facility':'Chennai Assembly Plant','category':'Motors','predicted':11.0,'cost_lakh':22.0,'co2_reduction_t':214,'downtime_days':4,'risk':'Medium','evidence':74,'status':'Hypothesis'},
 {'id':'water','name':'Closed-loop water recirculation','facility':'Chennai Assembly Plant','category':'Water','predicted':18.0,'cost_lakh':28.0,'co2_reduction_t':42,'downtime_days':3,'risk':'Medium','evidence':68,'status':'Hypothesis'}]


def fresh():
 return {'organization':{'name':'Aster Components Pvt Ltd','period':'Jan 2025 – Aug 2026','currency':'INR'},'facilities':FACILITIES,
 'overview':{'co2e_t':6428,'co2e_change':-6.4,'energy_mwh':11820,'water_ml':47.2,'waste_t':284,'data_readiness':86,'verified_impact_t':241,'active_pilots':2,'trend':[721,704,690,681,653,638,612,601,577,563,548,526]},
 'hotspots':[{'rank':1,'facility':'Chennai Assembly Plant','resource':'HVAC electricity','scope':'Scope 2','impact_t':1842,'contribution':28.7,'trend':4.2,'intensity':94.6},{'rank':2,'facility':'Hosur Manufacturing Plant','resource':'Process electricity','scope':'Scope 2','impact_t':1514,'contribution':23.6,'trend':-1.8,'intensity':81.2},{'rank':3,'facility':'Hosur Manufacturing Plant','resource':'Diesel generation','scope':'Scope 1','impact_t':908,'contribution':14.1,'trend':2.7,'intensity':37.4},{'rank':4,'facility':'Bengaluru Distribution Centre','resource':'Logistics fuel','scope':'Scope 3','impact_t':642,'contribution':10.0,'trend':-3.1,'intensity':22.8}],
 'interventions':INTERVENTIONS,
 'contract':{'id':'contract-hvac-chennai','status':'ready','revision':3,'intervention':'HVAC scheduling optimisation','facility':'Chennai Assembly Plant','hypothesis':'Reducing after-hours HVAC operation will lower electricity intensity without reducing production performance or thermal comfort.','primary_kpi':'kWh per 1,000 units produced','secondary_kpis':['Total electricity','Electricity cost','Scope 2 emissions','Indoor temperature'],'predicted_effect':14,'minimum_success_threshold':8,'baseline':'01 Jan 2026 – 31 Mar 2026','pilot':'01 Apr 2026 – 28 Apr 2026','control':'Hosur Manufacturing Plant — matched production weeks','confounders':['Production volume','Outside temperature','Operating hours','Shift pattern'],'guardrails':['Production ≥ 98% of plan','Temperature 22–26°C','Unplanned downtime = 0','Quality rejection increase ≤ 0.5%'],'required_evidence':['15-minute smart-meter readings','Daily production records','Operating-hour log','Weather observations'],'approver':'Priya Raman · VP Operations'},
 'proof':{'id':'proof-hvac-chennai','intervention':'HVAC scheduling optimisation','facility':'Chennai Assembly Plant','status':'VERIFIED','predicted_effect':14.0,'verified_effect':10.3,'prediction_error':3.7,'absolute_effect_mwh':-31.8,'absolute_change':-3.1,'production_change':8.1,'intensity_change':-10.3,'observed_post':82.4,'counterfactual_post':91.9,'confidence_interval':[-12.8,-7.7],'method':'Difference-in-Differences, production-normalised','assumptions':['Hosur provides a stable parallel trend','No overlapping energy intervention began during the pilot','Meter and production records use aligned weekly periods'],'diagnostics':{'pretrend_p':.34,'r_squared':.87,'weeks':30},'series':series()},
 'gate':{'score':91,'label':'Decision-grade','status':'VERIFIED','missing':[]},
 'rebound':{'type':'PARTIAL REBOUND / PRODUCTION OFFSET','severity':'warning','message':'Efficiency improved, but production growth absorbed a substantial portion of the expected absolute saving.'},
 'calibration':{'factor':.84,'mean_absolute_error':3.0},
 'transferability':{'score':84,'recommendation':'Run a limited pilot before transfer','largest_mismatches':['Resource Context','Climate'],'dimensions':{'equipment':91,'operations':84,'climate':77,'production':88,'resource_context':72,'implementation':92}},
 'memory':[{'name':'HVAC optimisation','predicted':14.0,'verified':10.3,'facility':'Chennai','status':'Verified'},{'name':'LED retrofit','predicted':21.0,'verified':18.8,'facility':'Bengaluru','status':'Verified'},{'name':'Motor optimisation','predicted':11.0,'verified':11.7,'facility':'Hosur','status':'Verified'},{'name':'Solar installation','predicted':25.0,'verified':19.5,'facility':'Chennai','status':'Estimated'}],
 'evidence':[{'id':'EVD-1042','title':'Chennai main meter · weekly aggregate','source':'Schneider PM8000','method':'Meter aggregation','date':'28 Aug 2026','status':'Validated'},{'id':'EVD-1038','title':'Production output · Line A','source':'MES export','method':'Unit normalization','date':'27 Aug 2026','status':'Validated'},{'id':'EVD-1029','title':'Hosur matched control series','source':'Operations data lake','method':'Parallel-trend test','date':'26 Aug 2026','status':'Validated'},{'id':'EVD-1017','title':'Grid emission factor · demo 2025','source':'Illustrative factor library','method':'Quantity × factor','date':'20 Aug 2026','status':'Demo factor'}],
 'audit':[{'event':'Proof run completed','detail':'HVAC verified at −10.3%','time':'Today · 10:42'},{'event':'Evidence gate passed','detail':'Score 91 / 100','time':'Today · 10:41'},{'event':'Pilot replayed','detail':'Predetermined 28-day measurement set','time':'Today · 10:38'}]}


STATE=fresh()
class Handler(BaseHTTPRequestHandler):
 def end_headers(self):
  self.send_header('Access-Control-Allow-Origin','http://127.0.0.1:4173'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS'); super().end_headers()
 def send(self,obj,status=200):
  data=json.dumps(obj,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
 def body(self):
  raw=self.rfile.read(int(self.headers.get('Content-Length','0'))); return raw.decode('utf-8')
 def do_OPTIONS(self): self.send_response(204); self.end_headers()
 def do_GET(self):
  if self.path=='/health': self.send({'status':'ok','database':'connected'})
  elif self.path=='/api/demo': self.send(STATE)
  else: self.send({'detail':'Not found'},404)
 def do_POST(self):
  global STATE
  if self.path=='/api/demo/reset': STATE=fresh(); self.send({'ok':True,'state':STATE})
  elif self.path.endswith('/approve'): STATE['contract']['status']='approved'; STATE['contract']['revision']+=1; self.send(STATE['contract'])
  elif self.path.endswith('/start'):
   if STATE['contract']['status']!='approved': self.send({'detail':'Approval is required before starting the pilot'},409)
   else: STATE['contract']['status']='running'; self.send(STATE['contract'])
  elif self.path=='/api/pilots/replay': STATE['contract']['status']='completed'; self.send({'ok':True,'proof_id':STATE['proof']['id'],'status':'VERIFIED'})
  elif self.path=='/api/scenarios/simulate':
   p=json.loads(self.body() or '{}'); selected=[i for i in INTERVENTIONS if i['id'] in p.get('selected_ids',[]) ] or [INTERVENTIONS[0]]; cost=sum(i['cost_lakh'] for i in selected); benefit=round(sum(i['co2_reduction_t'] for i in selected)/65,1); save=round(sum(i['co2_reduction_t'] for i in selected)*.074,1); self.send({'feasible':cost<=p.get('budget_lakh',0),'capex_lakh':cost,'co2_reduction':benefit,'annual_savings_lakh':save,'payback_years':round(cost/save,1),'energy_reduction':round(benefit*1.18,1),'water_change':0,'target_met':benefit>=p.get('target_reduction',0)})
  elif self.path=='/api/portfolio/optimize':
   p=json.loads(self.body() or '{}'); budget=p.get('budget_lakh',45); chosen=[]; cost=impact=0
   for i in sorted(INTERVENTIONS,key=lambda x:x['co2_reduction_t']/x['cost_lakh'],reverse=True):
    if cost+i['cost_lakh']<=budget: chosen.append(i['name']); cost+=i['cost_lakh']; impact+=i['co2_reduction_t']
   self.send({'selected':chosen,'total_cost_lakh':round(cost,1),'impact_t':round(impact,1),'unused_budget_lakh':round(budget-cost,1)})
  elif self.path=='/api/transferability':
   p=json.loads(self.body() or '{}'); self.send(STATE['transferability'] if p.get('target_facility')=='hosur' else {'score':65,'recommendation':'High uncertainty; redesign the pilot','largest_mismatches':['Production','Operations'],'dimensions':{'equipment':64,'operations':58,'climate':86,'production':55,'resource_context':69,'implementation':73}})
  elif self.path=='/api/imports/validate':
   text=self.body(); reader=csv.DictReader(io.StringIO(text)); rows=list(reader); self.send({'imported':len(rows),'warnings':0,'rejected':0,'errors':[],'preview':rows[:5]})
  else: self.send({'detail':'Not found'},404)
 def log_message(self,format,*args): pass

if __name__=='__main__':
 print('EcoMind API running at http://127.0.0.1:8000',flush=True); ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
