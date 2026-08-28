CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE organizations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  currency char(3) NOT NULL DEFAULT 'INR',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  email text NOT NULL UNIQUE,
  role text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE facilities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  name text NOT NULL,
  facility_type text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE data_sources (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  facility_id uuid REFERENCES facilities(id),
  name text NOT NULL,
  provenance jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE activity_records (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  facility_id uuid NOT NULL REFERENCES facilities(id),
  data_source_id uuid REFERENCES data_sources(id),
  activity_date date NOT NULL,
  metric text NOT NULL,
  quantity numeric NOT NULL CHECK (quantity >= 0),
  unit text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE emission_factors (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid REFERENCES organizations(id),
  category text NOT NULL,
  factor numeric NOT NULL,
  unit text NOT NULL,
  scope text NOT NULL,
  version text NOT NULL,
  source text NOT NULL,
  factor_year integer NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE emission_results (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  activity_record_id uuid NOT NULL REFERENCES activity_records(id),
  factor_id uuid NOT NULL REFERENCES emission_factors(id),
  kg_co2e numeric NOT NULL,
  formula text NOT NULL,
  assumptions jsonb NOT NULL DEFAULT '[]',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE interventions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  facility_id uuid NOT NULL REFERENCES facilities(id),
  name text NOT NULL,
  category text NOT NULL,
  status text NOT NULL,
  required_evidence jsonb NOT NULL DEFAULT '[]',
  possible_side_effects jsonb NOT NULL DEFAULT '[]',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE intervention_predictions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  intervention_id uuid NOT NULL REFERENCES interventions(id),
  predicted_effect numeric NOT NULL,
  calibrated_effect numeric,
  model_metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE scenarios (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  name text NOT NULL,
  constraints jsonb NOT NULL,
  result jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE decision_contracts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  intervention_id uuid NOT NULL REFERENCES interventions(id),
  revision integer NOT NULL DEFAULT 1,
  status text NOT NULL,
  hypothesis text NOT NULL,
  primary_kpi text NOT NULL,
  secondary_kpis jsonb NOT NULL DEFAULT '[]',
  baseline_period daterange,
  pilot_period daterange,
  guardrails jsonb NOT NULL DEFAULT '[]',
  confounders jsonb NOT NULL DEFAULT '[]',
  measurement_plan jsonb NOT NULL DEFAULT '{}',
  approval jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE pilot_plans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  contract_id uuid NOT NULL REFERENCES decision_contracts(id),
  scope jsonb NOT NULL,
  control_strategy jsonb NOT NULL,
  stop_criteria jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE measurements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  pilot_plan_id uuid NOT NULL REFERENCES pilot_plans(id),
  measured_at timestamptz NOT NULL,
  metric text NOT NULL,
  value numeric NOT NULL,
  unit text NOT NULL,
  provenance jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE causal_runs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  pilot_plan_id uuid NOT NULL REFERENCES pilot_plans(id),
  method text NOT NULL,
  result jsonb NOT NULL,
  assumptions jsonb NOT NULL DEFAULT '[]',
  diagnostics jsonb NOT NULL DEFAULT '{}',
  evidence_status text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE rebound_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  causal_run_id uuid NOT NULL REFERENCES causal_runs(id),
  event_type text NOT NULL,
  severity text NOT NULL,
  result jsonb NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE decision_memory (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  intervention_id uuid NOT NULL REFERENCES interventions(id),
  causal_run_id uuid REFERENCES causal_runs(id),
  prediction_error numeric,
  reliability_ratio numeric,
  lessons jsonb NOT NULL DEFAULT '[]',
  transfer_tags jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE evidence_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  title text NOT NULL,
  source text NOT NULL,
  method text NOT NULL,
  assumptions jsonb NOT NULL DEFAULT '[]',
  result jsonb NOT NULL DEFAULT '{}',
  embedding vector(1536),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE kg_nodes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  node_type text NOT NULL,
  label text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE kg_edges (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  source_id uuid NOT NULL REFERENCES kg_nodes(id),
  target_id uuid NOT NULL REFERENCES kg_nodes(id),
  edge_type text NOT NULL,
  metadata jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE audit_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL REFERENCES organizations(id),
  actor_id uuid REFERENCES users(id),
  event_type text NOT NULL,
  entity_type text NOT NULL,
  entity_id uuid,
  details jsonb NOT NULL DEFAULT '{}',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX activity_org_facility_date_idx ON activity_records (organization_id, facility_id, activity_date);
CREATE INDEX evidence_org_created_idx ON evidence_items (organization_id, created_at DESC);
CREATE INDEX kg_node_metadata_idx ON kg_nodes USING gin (metadata);
CREATE INDEX kg_edge_org_source_idx ON kg_edges (organization_id, source_id);

