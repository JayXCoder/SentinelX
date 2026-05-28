export type IntelligenceSignal = {
  id: string;
  signal_type: 'cyber' | 'gtm' | 'financial' | 'vendor_risk' | 'osint' | 'executive_summary';
  category: string;
  title: string;
  summary: string;
  entities: string[];
  severity: number;
  confidence: number;
  source_reliability: number;
  evidence: string[];
  recommended_action?: string;
  created_at: string;
};

export type RiskScore = {
  id: string;
  entity_id: string;
  entity_name: string;
  score_type: string;
  score_value: number;
  risk_level: 'low' | 'medium' | 'high' | 'critical';
  explanation: string;
  calculated_at: string;
};

export type CorrelatedEvent = {
  id: string;
  event_type: string;
  title: string;
  summary: string;
  involved_entities: string[];
  signal_ids: string[];
  correlation_reason: string;
  confidence: number;
  severity: number;
  first_seen: string;
  last_seen: string;
};

export type RagAnswer = {
  answer: string;
  confidence: number;
  supporting_evidence: string[];
  related_entities: string[];
  related_events: string[];
  recommended_action?: string;
};
