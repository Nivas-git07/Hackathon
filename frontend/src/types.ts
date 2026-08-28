export type Facility = { id: string; name: string; type: string; city: string; readiness: number }
export type Intervention = { id: string; name: string; facility: string; category: string; predicted: number; cost_lakh: number; co2_reduction_t: number; downtime_days: number; risk: string; evidence: number; status: string }
export type DemoData = {
  organization: { name: string; period: string; currency: string }
  facilities: Facility[]
  overview: { co2e_t: number; co2e_change: number; energy_mwh: number; water_ml: number; waste_t: number; data_readiness: number; verified_impact_t: number; active_pilots: number; trend: number[] }
  hotspots: Array<{ rank: number; facility: string; resource: string; scope: string; impact_t: number; contribution: number; trend: number; intensity: number }>
  interventions: Intervention[]
  contract: { id: string; status: string; revision: number; intervention: string; facility: string; hypothesis: string; primary_kpi: string; secondary_kpis: string[]; predicted_effect: number; minimum_success_threshold: number; baseline: string; pilot: string; control: string; confounders: string[]; guardrails: string[]; required_evidence: string[]; approver: string }
  proof: { id: string; intervention: string; facility: string; status: string; predicted_effect: number; verified_effect: number; prediction_error: number; absolute_effect_mwh: number; absolute_change: number; production_change: number; intensity_change: number; observed_post: number; counterfactual_post: number; confidence_interval: number[]; method: string; assumptions: string[]; diagnostics: Record<string, number>; series: Array<{ date: string; actual: number; counterfactual: number | null; predicted: number | null; lower: number | null; upper: number | null; production: number }> }
  gate: { score: number; label: string; status: string; missing: string[] }
  rebound: { type: string; severity: string; message: string }
  calibration: { factor: number; mean_absolute_error: number }
  transferability: TransferResult
  memory: Array<{ name: string; predicted: number; verified: number; facility: string; status: string }>
  evidence: Array<{ id: string; title: string; source: string; method: string; date: string; status: string }>
  audit: Array<{ event: string; detail: string; time: string }>
}
export type ScenarioResult = { feasible: boolean; capex_lakh: number; co2_reduction: number; annual_savings_lakh: number; payback_years: number | null; energy_reduction: number; water_change: number; target_met: boolean }
export type TransferResult = { score: number; recommendation: string; largest_mismatches: string[]; dimensions: Record<string, number> }

