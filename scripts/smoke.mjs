import { readFile } from 'node:fs/promises';

const api = 'http://127.0.0.1:8003';
const ui = 'http://127.0.0.1:4174';

async function json(path, options) {
  const response = await fetch(api + path, options);
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

function post(body) {
  return { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) };
}

const health = await json('/health');
await json('/api/demo/reset', { method: 'POST' });
const empty = await json('/api/demo');
if (health.status !== 'ok' || empty.has_data !== false || empty.overview.co2e_t !== 0) throw new Error('Empty bootstrap failed');

const csv = await readFile(new URL('../runtime/ecomind-20-row-emissions.csv', import.meta.url), 'utf8');
const upload = await json('/api/imports/validate', { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: csv });
const demo = await json('/api/demo');
if (upload.imported !== 20 || upload.warnings !== 0 || demo.has_data !== true || demo.overview.co2e_t <= 0 || demo.hotspots.length === 0) throw new Error('CSV-driven analysis failed');
const persisted = JSON.parse(await readFile(new URL('../backend/data/current_state.json', import.meta.url), 'utf8'));
if (persisted.has_data !== true || persisted.analysis.rows !== 20) throw new Error('Persistent upload state failed');

const scenario = await json('/api/scenarios/simulate', post({
  energy_adjustment: -8,
  fuel_adjustment: -4,
  production_adjustment: 6,
}));
if (typeof scenario.projected_co2e !== 'number') throw new Error('Scenario simulator failed');

const portfolio = await json('/api/portfolio/optimize', post({
  budget_lakh: 45,
  target_reduction: 5,
  max_downtime: 7,
}));
if (!Array.isArray(portfolio.selected)) throw new Error('Portfolio optimizer failed');

const contract = await json('/api/contracts/contract-hvac-chennai/draft', post({
  hypothesis: demo.contract.hypothesis,
  minimum_success_threshold: demo.contract.minimum_success_threshold,
}));
if (contract.status !== 'ready') throw new Error('Decision contract draft failed');

for (const route of ['dashboard', 'data-center', 'sustainability', 'scenario-lab', 'interventions', 'optimization', 'decision-contracts', 'verification', 'decision-memory', 'insights']) {
  const response = await fetch(`${ui}/${route}`);
  const html = await response.text();
  if (!response.ok || !html.includes('EcoMind — Simple Sustainability Guide')) throw new Error(`Route /${route} failed`);
}

const sample = await fetch(`${ui}/ecomind-20-row-emissions.csv`);
const sampleText = await sample.text();
if (!sample.ok || !sampleText.startsWith('date,facility,stream,quantity,unit') || sampleText.trim().split(/\r?\n/).length !== 21) throw new Error('20-row CSV download failed');

await json('/api/demo/reset', { method: 'POST' });
const finalEmpty = await json('/api/demo');
if (finalEmpty.has_data !== false || finalEmpty.overview.co2e_t !== 0 || finalEmpty.data_quality.overall !== 0 || finalEmpty.hotspots.length !== 0) throw new Error('Final zero state failed');

console.log(JSON.stringify({
  status: 'ok',
  routes: 10,
  dataQuality: demo.data_quality.overall,
  uploadedRows: upload.imported,
  emissions: demo.overview.co2e_t,
  projectedCo2e: scenario.projected_co2e,
  optimizedActions: portfolio.selected.length,
  finalState: 'zero',
}));
