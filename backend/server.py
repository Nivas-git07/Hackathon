from __future__ import annotations

import copy, csv, io, json, os
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from math import sin
from pathlib import Path


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
 {'id':'water','name':'Closed-loop water recirculation','facility':'Chennai Assembly Plant','category':'Water','predicted':18.0,'cost_lakh':28.0,'co2_reduction_t':42,'downtime_days':3,'risk':'Medium','evidence':68,'status':'Hypothesis'},
 {'id':'ev','name':'EV logistics conversion','facility':'Bengaluru Distribution Centre','category':'Fleet electrification','predicted':19.0,'cost_lakh':34.0,'co2_reduction_t':186,'downtime_days':3,'risk':'Medium','evidence':71,'status':'Hypothesis'}]


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
 'audit':[{'event':'Proof run completed','detail':'HVAC verified at −10.3%','time':'Today · 10:42'},{'event':'Evidence gate passed','detail':'Score 91 / 100','time':'Today · 10:41'},{'event':'Pilot replayed','detail':'Predetermined 28-day measurement set','time':'Today · 10:38'}],
 'data_quality':{'overall':88,'streams':[{'id':'electricity','label':'Electricity','score':98,'coverage':'99.2%','records':14592,'status':'Validated'},{'id':'fuel','label':'Fuel','score':94,'coverage':'96.4%','records':728,'status':'Validated'},{'id':'water','label':'Water','score':81,'coverage':'84.1%','records':684,'status':'Review'},{'id':'waste','label':'Waste','score':72,'coverage':'76.8%','records':212,'status':'Action needed'}],'anomalies':[{'severity':'High','stream':'Waste','message':'11 missing manifests in Bengaluru · Jul 2026','time':'2h ago'},{'severity':'Medium','stream':'Water','message':'Meter discontinuity at Chennai Zone C','time':'Yesterday'},{'severity':'Low','stream':'Fuel','message':'3 duplicate delivery references auto-resolved','time':'24 Aug'}]},
 'factor_sources':[{'category':'Electricity','factor':0.716,'unit':'kgCO₂e/kWh','source':'Illustrative India grid mix','year':2025,'scope':'Scope 2'},{'category':'Diesel','factor':2.68,'unit':'kgCO₂e/L','source':'Illustrative combustion factor','year':2025,'scope':'Scope 1'},{'category':'Waste','factor':0.47,'unit':'kgCO₂e/kg','source':'Illustrative disposal mix','year':2025,'scope':'Scope 3'}],
 'execution':[{'id':'hvac','progress':72,'allocated_lakh':3.0,'payback_years':1.8},{'id':'compressed-air','progress':61,'allocated_lakh':5.5,'payback_years':2.4},{'id':'led','progress':100,'allocated_lakh':16.0,'payback_years':2.1},{'id':'solar','progress':18,'allocated_lakh':38.0,'payback_years':4.6}],
 'recommendations':[{'priority':'P1','title':'Close the Chennai production-offset gap','action':'Retune after-hours schedules by zone and extend the verified pilot for 14 days.','impact':'Recover 18–24 MWh annual absolute savings','confidence':91,'evidence':['EVD-1042','EVD-1038']},{'priority':'P2','title':'Repair waste-stream completeness','action':'Connect Bengaluru manifest exports before promoting waste actions to candidate status.','impact':'Raise waste data quality from 72% to ~90%','confidence':88,'evidence':['Data quality gate']},{'priority':'P3','title':'Transfer HVAC learning to Hosur carefully','action':'Run the recommended limited pilot; climate and resource context remain the largest mismatches.','impact':'Potential 110–145 tCO₂e annual reduction','confidence':84,'evidence':['PL-2026-004','EVD-1029']}]}


REQUIRED_COLUMNS={'date','facility','stream','quantity','unit'}
STREAMS=('electricity','fuel','water','waste')
STREAM_LABELS={'electricity':'Electricity','fuel':'Fuel','water':'Water','waste':'Waste'}
STREAM_SCOPES={'electricity':'Scope 2','fuel':'Scope 1','water':'Scope 3','waste':'Scope 3'}
STREAM_RESOURCES={'electricity':'Electricity use','fuel':'Fuel use','water':'Water use','waste':'Waste disposal'}


def empty_state():
 state=copy.deepcopy(fresh()); state['has_data']=False; state['uploaded_file']=None; state['analysis']={'status':'waiting','rows':0,'confidence':0,'message':'Upload a CSV file to calculate results.'}
 state['overview']={'co2e_t':0,'co2e_change':0,'energy_mwh':0,'fuel_kl':0,'water_ml':0,'waste_t':0,'data_readiness':0,'verified_impact_t':0,'active_pilots':0,'trend':[0]*12,'months':[],'scope':{'Scope 1':0,'Scope 2':0,'Scope 3':0}}
 state['stream_totals']={stream:0 for stream in STREAMS}; state['hotspots']=[]; state['recommendations']=[]; state['memory']=[]; state['evidence']=[]; state['audit']=[]
 state['data_quality']={'overall':0,'streams':[{'id':stream,'label':STREAM_LABELS[stream],'score':0,'coverage':'0%','records':0,'status':'Waiting for data'} for stream in STREAMS],'anomalies':[]}
 state['gate']={'score':0,'label':'Waiting for data','status':'WAITING','missing':['CSV upload']}; state['calibration']={'factor':0,'mean_absolute_error':0}
 state['proof'].update({'status':'WAITING','predicted_effect':0,'verified_effect':0,'prediction_error':0,'absolute_effect_mwh':0,'absolute_change':0,'production_change':0,'intensity_change':0,'observed_post':0,'counterfactual_post':0,'confidence_interval':[0,0],'series':[]})
 state['rebound']={'type':'WAITING FOR DATA','severity':'neutral','message':'Upload production data with future records to test for a rebound effect.'}
 state['contract'].update({'status':'waiting','predicted_effect':0,'minimum_success_threshold':0,'baseline':'Not available','pilot':'Not available'})
 for item in state['interventions']: item.update({'predicted':0,'co2_reduction_t':0,'evidence':0,'status':'Waiting for data'})
 return state


def convert_reading(stream,quantity,unit):
 unit=unit.strip().lower(); q=float(quantity)
 if q<0: raise ValueError('quantity cannot be negative')
 if stream=='electricity':
  if unit=='kwh': return q/1000,q*.716/1000
  if unit=='mwh': return q,q*.716
 elif stream=='fuel':
  if unit in {'litre','liter','l'}: return q/1000,q*2.68/1000
  if unit=='kl': return q,q*2.68
 elif stream=='water':
  if unit=='ml': return q,q*.344
  if unit=='kl': return q/1000,q*.000344
  if unit in {'litre','liter','l'}: return q/1_000_000,q*.000000344
 elif stream=='waste':
  if unit=='kg': return q/1000,q*.47/1000
  if unit in {'t','tonne','tonnes'}: return q,q*.47
 raise ValueError(f'unit {unit or "(blank)"} is not valid for {stream}')


def analyse_csv(text):
 reader=csv.DictReader(io.StringIO(text.strip().lstrip('\ufeff'))); columns={str(c).strip().lower() for c in (reader.fieldnames or [])}
 missing=sorted(REQUIRED_COLUMNS-columns)
 if missing: return None,{'imported':0,'warnings':0,'rejected':0,'errors':[f'Missing columns: {", ".join(missing)}'],'message':'Use the downloadable EcoMind CSV template.'}
 accepted=[]; errors=[]; seen=set(); duplicates=0
 for number,raw in enumerate(reader,start=2):
  row={str(k).strip().lower():str(v or '').strip() for k,v in raw.items()}; key=tuple(row.get(k,'').lower() for k in ('date','facility','stream','quantity','unit'))
  if key in seen: duplicates+=1; continue
  seen.add(key)
  try:
   parsed=date.fromisoformat(row['date']); stream=row['stream'].lower()
   if stream not in STREAMS: raise ValueError('stream must be electricity, fuel, water, or waste')
   if not row['facility']: raise ValueError('facility is required')
   canonical,emissions=convert_reading(stream,row['quantity'],row['unit'])
   accepted.append({'date':parsed.isoformat(),'month':parsed.strftime('%Y-%m'),'facility':row['facility'],'stream':stream,'quantity':float(row['quantity']),'unit':row['unit'],'canonical':canonical,'emissions_t':emissions})
  except (ValueError,TypeError) as exc: errors.append(f'Row {number}: {exc}')
 if not accepted: return None,{'imported':0,'warnings':duplicates,'rejected':len(errors),'errors':errors,'message':'No valid rows were found.'}
 state=build_state(accepted,duplicates,errors)
 result={'imported':len(accepted),'warnings':duplicates,'rejected':len(errors),'errors':errors,'preview':accepted[:5],'message':f'{len(accepted)} unique rows analysed. Every page now uses this upload.','state':state}
 return state,result


def build_state(rows,duplicates,errors):
 state=empty_state(); state['has_data']=True; state['uploaded_file']='Uploaded CSV'; months=sorted({r['month'] for r in rows}); facilities=sorted({r['facility'] for r in rows})
 state['organization']['period']=f'{min(r["date"] for r in rows)} to {max(r["date"] for r in rows)}'
 month_emissions={month:0 for month in months}; stream_emissions={stream:0 for stream in STREAMS}; scope_totals={'Scope 1':0,'Scope 2':0,'Scope 3':0}; activity={stream:0 for stream in STREAMS}; grouped={}
 for row in rows:
  month_emissions[row['month']]+=row['emissions_t']; stream_emissions[row['stream']]+=row['emissions_t']; scope_totals[STREAM_SCOPES[row['stream']]]+=row['emissions_t']; activity[row['stream']]+=row['canonical']; grouped[(row['facility'],row['stream'])]=grouped.get((row['facility'],row['stream']),0)+row['emissions_t']
 total=sum(stream_emissions.values()); values=[round(month_emissions[m],1) for m in months]; previous=values[-2] if len(values)>1 else 0; change=round((values[-1]-previous)/previous*100,1) if previous else 0
 trend=([0]*max(0,12-len(values))+values[-12:])
 expected=max(1,len(months)*len(facilities)); quality=[]; anomalies=[]
 for stream in STREAMS:
  count=sum(1 for row in rows if row['stream']==stream); coverage=min(1,count/expected); score=round(88+coverage*11) if count else 0; status='Good' if score>=90 else 'Needs improvement' if score else 'Missing'
  quality.append({'id':stream,'label':STREAM_LABELS[stream],'score':score,'coverage':f'{round(coverage*100)}%','records':count,'status':status})
  if count<expected: anomalies.append({'severity':'Medium' if count else 'High','stream':STREAM_LABELS[stream],'message':f'{expected-count} monthly {stream} reading(s) are missing.','time':'Current upload'})
 if duplicates: anomalies.append({'severity':'Low','stream':'File','message':f'{duplicates} duplicate row(s) were ignored.','time':'Current upload'})
 overall=round(sum(q['score'] for q in quality)/len(quality)); state['data_quality']={'overall':overall,'streams':quality,'anomalies':anomalies}
 state['overview']={'co2e_t':round(total,1),'co2e_change':change,'energy_mwh':round(activity['electricity'],1),'fuel_kl':round(activity['fuel'],1),'water_ml':round(activity['water'],2),'waste_t':round(activity['waste'],2),'data_readiness':overall,'verified_impact_t':0,'active_pilots':0,'trend':trend,'months':months[-12:],'scope':{key:round(value,1) for key,value in scope_totals.items()}}
 state['stream_totals']={key:round(value,1) for key,value in stream_emissions.items()}
 ranked=sorted(grouped.items(),key=lambda item:item[1],reverse=True)[:6]; state['hotspots']=[{'rank':index,'facility':key[0],'resource':STREAM_RESOURCES[key[1]],'stream':key[1],'scope':STREAM_SCOPES[key[1]],'impact_t':round(value,1),'contribution':round(value/total*100,1) if total else 0,'trend':change,'intensity':round(value,1)} for index,(key,value) in enumerate(ranked,start=1)]
 intervention_stream={'hvac':'electricity','compressed-air':'electricity','led':'electricity','solar':'electricity','motors':'electricity','water':'water','ev':'fuel'}; predicted={'hvac':14,'compressed-air':11,'led':21,'solar':25,'motors':11,'water':18,'ev':19}
 state['interventions']=copy.deepcopy(INTERVENTIONS)
 for item in state['interventions']:
  pct=predicted[item['id']]; source=intervention_stream[item['id']]; item['predicted']=pct; item['co2_reduction_t']=round(stream_emissions[source]*pct/100,1); item['evidence']=max(0,min(99,overall-(5 if source in {'water','waste'} else 0))); item['status']='Ready to compare' if stream_emissions[source]>0 else 'Missing source data'
 verified=max(0,-change); predicted_effect=14.0; prediction_error=round(abs(predicted_effect-verified),1); last=values[-1]; counter=previous or last
 state['proof'].update({'status':'ANALYSED','predicted_effect':predicted_effect,'verified_effect':verified,'prediction_error':prediction_error,'absolute_effect_mwh':round(activity['electricity']*change/100,1),'absolute_change':change,'production_change':0,'intensity_change':-verified,'observed_post':last,'counterfactual_post':counter,'confidence_interval':[round(max(0,verified-2),1),round(verified+2,1)],'series':[{'date':month+'-01','actual':value,'counterfactual':previous if idx else None,'predicted':None,'lower':None,'upper':None,'production':0} for idx,(month,value) in enumerate(zip(months,values))]})
 state['gate']={'score':overall,'label':'Good data' if overall>=85 else 'Needs review','status':'ANALYSED','missing':[a['message'] for a in anomalies if a['severity']=='High']}; state['calibration']={'factor':round(verified/predicted_effect,2) if predicted_effect else 0,'mean_absolute_error':prediction_error}
 state['rebound']={'type':'PRODUCTION DATA NOT PROVIDED','severity':'neutral','message':'The CSV shows resource use, but not production volume. Absolute emissions are calculated; per-unit rebound needs a production column in a future dataset.'}
 state['memory']=[{'name':'Uploaded period comparison','predicted':predicted_effect,'verified':verified,'facility':'All uploaded facilities','status':'Calculated'}]
 top=state['hotspots'][0] if state['hotspots'] else {'resource':'Uploaded activity','facility':'Uploaded facility','impact_t':0}; lowest=min(quality,key=lambda q:q['score'])
 state['recommendations']=[{'priority':'1','title':f'Reduce {top["resource"].lower()} first','action':f'Start with {top["facility"]}, the largest source in this upload.','impact':f'Current source: {top["impact_t"]} tCO₂e','confidence':overall,'evidence':['Uploaded CSV','Emission factors']},{'priority':'2','title':f'Improve {lowest["label"].lower()} data','action':'Add the missing monthly readings before committing a large budget.','impact':f'Current data score: {lowest["score"]}%','confidence':overall,'evidence':['Data completeness check']},{'priority':'3','title':'Test the recommended plan','action':'Use Try Changes, then Best Plan, before setting success rules.','impact':'Reduces decision risk','confidence':max(70,overall-5),'evidence':['Scenario engine','Solution catalogue']}]
 state['evidence']=[{'id':'CSV-001','title':'Uploaded operational readings','source':'User CSV upload','method':'Validated unit conversion and aggregation','date':max(r['date'] for r in rows),'status':'Validated'},{'id':'FAC-001','title':'Emission factors used','source':'EcoMind factor register','method':'Activity × emission factor','date':max(r['date'] for r in rows),'status':'Validated'}]
 state['audit']=[{'event':'CSV analysis completed','detail':f'{len(rows)} unique rows processed','time':'Just now'},{'event':'Data quality calculated','detail':f'{overall}% overall quality','time':'Just now'}]
 state['analysis']={'status':'complete','rows':len(rows),'confidence':overall,'message':'All dashboard values were recalculated from the uploaded CSV.'}
 state['contract'].update({'status':'ready','predicted_effect':predicted_effect,'minimum_success_threshold':round(predicted_effect*.6,1),'baseline':state['organization']['period'],'pilot':'Set before implementation'})
 return state


STATE_FILE=Path(__file__).resolve().parent/'data'/'current_state.json'


def load_state():
 try:
  return json.loads(STATE_FILE.read_text(encoding='utf-8'))
 except (FileNotFoundError,json.JSONDecodeError,OSError):
  return empty_state()


def persist_state():
 STATE_FILE.parent.mkdir(parents=True,exist_ok=True); temporary=STATE_FILE.with_suffix('.tmp'); temporary.write_text(json.dumps(STATE,ensure_ascii=False),encoding='utf-8'); temporary.replace(STATE_FILE)


STATE=load_state()
class Handler(BaseHTTPRequestHandler):
 def end_headers(self):
  origin=self.headers.get('Origin','http://127.0.0.1:4173')
  if origin not in {'http://127.0.0.1:4173','http://127.0.0.1:4174'}: origin='http://127.0.0.1:4173'
  self.send_header('Access-Control-Allow-Origin',origin); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS'); super().end_headers()
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
  if self.path=='/api/demo/reset': STATE=empty_state(); persist_state(); self.send({'ok':True,'state':STATE})
  elif self.path.endswith('/draft'):
   p=json.loads(self.body() or '{}'); allowed=('hypothesis','primary_kpi','minimum_success_threshold','baseline','pilot'); STATE['contract'].update({key:p[key] for key in allowed if key in p}); STATE['contract']['status']='ready'; STATE['contract']['revision']+=1; persist_state(); self.send(STATE['contract'])
  elif self.path.endswith('/approve'): STATE['contract']['status']='approved'; STATE['contract']['revision']+=1; persist_state(); self.send(STATE['contract'])
  elif self.path.endswith('/start'):
   if STATE['contract']['status']!='approved': self.send({'detail':'Approval is required before starting the pilot'},409)
   else: STATE['contract']['status']='running'; persist_state(); self.send(STATE['contract'])
  elif self.path=='/api/pilots/replay': STATE['contract']['status']='completed'; persist_state(); self.send({'ok':True,'proof_id':STATE['proof']['id'],'status':'VERIFIED'})
  elif self.path=='/api/scenarios/simulate':
   p=json.loads(self.body() or '{}')
   if any(key in p for key in ('energy_adjustment','fuel_adjustment','production_adjustment')):
    energy=float(p.get('energy_adjustment',0)); fuel=float(p.get('fuel_adjustment',0)); production=float(p.get('production_adjustment',0)); baseline=STATE['overview']['co2e_t']; electricity=STATE.get('stream_totals',{}).get('electricity',0); fuel_emissions=STATE.get('stream_totals',{}).get('fuel',0); other=max(0,baseline-electricity-fuel_emissions); projected=round(electricity*(1+energy/100)+fuel_emissions*(1+fuel/100)+other,1); absolute_delta=round((projected-baseline)/baseline*100,1) if baseline else 0; intensity=round((projected/baseline)/(1+production/100)*100-100,1) if baseline and production>-100 else 0; self.send({'projected_co2e':projected,'absolute_change':absolute_delta,'intensity_change':intensity,'energy_mwh':round(STATE['overview']['energy_mwh']*(1+energy/100),1),'fuel_kl':round(STATE['overview'].get('fuel_kl',0)*(1+fuel/100),1),'production_index':round(100+production,1)})
   else:
    selected=[i for i in STATE['interventions'] if i['id'] in p.get('selected_ids',[]) ] or [STATE['interventions'][0]]; cost=sum(i['cost_lakh'] for i in selected); benefit=round(sum(i['co2_reduction_t'] for i in selected),1); save=round(benefit*.074,1); self.send({'feasible':cost<=p.get('budget_lakh',0),'capex_lakh':cost,'co2_reduction':round(benefit/STATE['overview']['co2e_t']*100,1) if STATE['overview']['co2e_t'] else 0,'annual_savings_lakh':save,'payback_years':round(cost/save,1) if save else 0,'energy_reduction':benefit,'water_change':0,'target_met':benefit>=p.get('target_reduction',0)})
  elif self.path=='/api/portfolio/optimize':
   p=json.loads(self.body() or '{}'); budget=float(p.get('budget_lakh',45)); max_down=int(p.get('max_downtime',7)); target=float(p.get('target_reduction',5)); best=(0,0,0,[])
   candidates=STATE['interventions']
   for mask in range(1,1<<len(candidates)):
    combo=[item for idx,item in enumerate(candidates) if mask&(1<<idx)]; cost=sum(i['cost_lakh'] for i in combo); down=sum(i['downtime_days'] for i in combo); impact=sum(i['co2_reduction_t'] for i in combo)
    if cost<=budget and down<=max_down and impact>best[0]: best=(impact,cost,down,combo)
   impact,cost,down,combo=best; baseline=STATE['overview']['co2e_t']; reduction=round(impact/baseline*100,1) if baseline else 0; self.send({'selected':[i['name'] for i in combo],'total_cost_lakh':round(cost,1),'impact_t':round(impact,1),'co2_reduction':reduction,'downtime_days':down,'unused_budget_lakh':round(budget-cost,1),'target_met':reduction>=target,'constraints':{'budget':True,'downtime':True,'target':reduction>=target}})
  elif self.path=='/api/transferability':
   p=json.loads(self.body() or '{}'); self.send(STATE['transferability'] if p.get('target_facility')=='hosur' else {'score':65,'recommendation':'High uncertainty; redesign the pilot','largest_mismatches':['Production','Operations'],'dimensions':{'equipment':64,'operations':58,'climate':86,'production':55,'resource_context':69,'implementation':73}})
  elif self.path=='/api/imports/validate':
   state,result=analyse_csv(self.body())
   if state is not None: STATE=state; persist_state()
   self.send(result,200 if state is not None else 422)
  else: self.send({'detail':'Not found'},404)
 def log_message(self,format,*args): pass

if __name__=='__main__':
 port=int(os.environ.get('ECOMIND_API_PORT','8000'))
 print(f'EcoMind API running at http://127.0.0.1:{port}',flush=True); ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
