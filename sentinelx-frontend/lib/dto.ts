import type { CorrelatedEvent, IntelligenceSignal, RagAnswer, RiskScore } from '@/types/sentinelx';

export type DashboardOverviewDto = {
  intelligence_signals: number;
  critical_alerts: number;
  vendor_risks: number;
  opportunity_score: number;
  summary: string;
};

export type ThreatFeedDto = IntelligenceSignal[];
export type CompetitorIntelligenceDto = IntelligenceSignal[];
export type VendorRiskDto = {
  summary: string;
  entities: RiskScore[];
};
export type AlertsDto = {
  active: Array<{ id: string; title: string; severity: string; created_at: string }>;
  resolved: Array<{ id: string; title: string; severity: string; created_at: string }>;
};
export type CorrelatedEventsDto = CorrelatedEvent[];
export type RagAnswerDto = RagAnswer;
