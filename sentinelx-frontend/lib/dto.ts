import type { CorrelatedEvent, IntelligenceSignal, RagAnswer, RiskScore } from '@/types/sentinelx';

export type DashboardOverviewDto = {
  intelligence_signals: number;
  critical_alerts: number;
  vendor_risks: number;
  opportunity_score: number;
  summary: string;
  correlated_events?: number;
  entities_tracked?: number;
};

export type AnalyticsOverviewDto = {
  total_signals_ingested: number;
  total_correlated_events: number;
  total_entities_tracked: number;
  total_risk_scores: number;
  critical_risks: number;
  high_risks: number;
};

export type TopRiskDto = {
  entity_id: string;
  entity_name: string;
  score_type: string;
  score_value: number;
  risk_level: RiskScore['risk_level'];
  explanation: string;
  calculated_at: string;
};

export type ThreatFeedDto = IntelligenceSignal[];
export type CompetitorIntelligenceDto = IntelligenceSignal[];
export type VendorRiskDto = {
  summary: string;
  entities: RiskScore[];
  byRiskLevel?: Record<string, string[]>;
};
export type AlertsDto = {
  active: Array<{
    id: string;
    title: string;
    severity: string;
    created_at: string;
    summary?: string;
    signal_type?: string;
  }>;
  resolved: Array<{ id: string; title: string; severity: string; created_at: string }>;
};
export type CorrelatedEventsDto = CorrelatedEvent[];
export type RagAnswerDto = RagAnswer;
