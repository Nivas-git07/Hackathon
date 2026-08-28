import type { DemoData, ScenarioResult, TransferResult } from './types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, options)
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: 'The request could not be completed' }))
    throw new Error(body.detail || 'The request could not be completed')
  }
  return response.json() as Promise<T>
}

export const api = {
  demo: () => request<DemoData>('/api/demo'),
  reset: () => request<{ ok: boolean; state: DemoData }>('/api/demo/reset', { method: 'POST' }),
  approve: (id: string) => request<DemoData['contract']>(`/api/contracts/${id}/approve`, { method: 'POST' }),
  start: (id: string) => request<DemoData['contract']>(`/api/contracts/${id}/start`, { method: 'POST' }),
  replay: () => request<{ ok: boolean; proof_id: string; status: string }>('/api/pilots/replay', { method: 'POST' }),
  scenario: (payload: object) => request<ScenarioResult>('/api/scenarios/simulate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  portfolio: (payload: object) => request<{ selected: string[]; total_cost_lakh: number; impact_t: number; unused_budget_lakh: number }>('/api/portfolio/optimize', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) }),
  transfer: (target_facility: string) => request<TransferResult>('/api/transferability', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ target_facility }) }),
  validateCsv: (content: string) => request<{ imported: number; warnings: number; rejected: number; errors: string[]; preview: Record<string, string>[] }>('/api/imports/validate', { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: content }),
}

