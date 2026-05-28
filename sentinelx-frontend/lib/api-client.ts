import type {
  AlertsDto,
  CompetitorIntelligenceDto,
  CorrelatedEventsDto,
  DashboardOverviewDto,
  RagAnswerDto,
  ThreatFeedDto,
  VendorRiskDto,
} from '@/lib/dto';
import type { CorrelatedEvent, IntelligenceSignal, RiskScore } from '@/types/sentinelx';

export type ApiError = {
  message: string;
  status: number;
  details?: unknown;
};

type ApiSignal = {
  id: string;
  parsed_record_id: string;
  signal_type: string;
  category: string;
  title: string;
  summary: string;
  entities: unknown[];
  severity: number;
  confidence: number;
  source_reliability: number;
  evidence: string[];
  recommended_action?: string | null;
  created_at: string;
};

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_URL ??
  'http://localhost:4000';

function mapSignal(signal: ApiSignal): IntelligenceSignal {
  return {
    id: String(signal.id),
    signal_type: signal.signal_type as IntelligenceSignal['signal_type'],
    category: signal.category,
    title: signal.title,
    summary: signal.summary,
    entities: (signal.entities ?? []).map((entity) =>
      typeof entity === 'string' ? entity : JSON.stringify(entity),
    ),
    severity: signal.severity,
    confidence: signal.confidence,
    source_reliability: signal.source_reliability,
    evidence: signal.evidence ?? [],
    recommended_action: signal.recommended_action ?? undefined,
    created_at: signal.created_at,
  };
}

function severityToRiskLevel(severity: number): RiskScore['risk_level'] {
  if (severity >= 8) return 'critical';
  if (severity >= 6) return 'high';
  if (severity >= 4) return 'medium';
  return 'low';
}

function toApiError(status: number, details?: unknown): ApiError {
  return {
    message: `Request failed: ${status}`,
    status,
    details,
  };
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    let details: unknown;
    try {
      details = await response.json();
    } catch {
      details = await response.text().catch(() => undefined);
    }
    throw toApiError(response.status, details);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

async function get<T>(path: string) {
  return request<T>(path, { method: 'GET' });
}

async function post<T>(path: string, body?: unknown) {
  return request<T>(path, {
    method: 'POST',
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

async function getSignals(signalType?: string, limit = 50): Promise<IntelligenceSignal[]> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (signalType) {
    params.set('signal_type', signalType);
  }
  const signals = await get<ApiSignal[]>(`/agents/signals?${params.toString()}`);
  return signals.map(mapSignal);
}

async function getDashboardOverview(): Promise<DashboardOverviewDto> {
  const signals = await getSignals(undefined, 100);
  const criticalAlerts = signals.filter((signal) => signal.severity >= 7).length;
  const vendorRisks = signals.filter((signal) => signal.signal_type === 'vendor_risk').length;
  const gtmSignals = signals.filter((signal) => signal.signal_type === 'gtm');
  const opportunityScore = gtmSignals.length
    ? Math.round(
        (gtmSignals.reduce((total, signal) => total + signal.confidence, 0) / gtmSignals.length) * 100,
      )
    : 0;
  const executiveSummary = signals.find((signal) => signal.signal_type === 'executive_summary');

  return {
    intelligence_signals: signals.length,
    critical_alerts: criticalAlerts,
    vendor_risks: vendorRisks,
    opportunity_score: opportunityScore,
    summary:
      executiveSummary?.summary ??
      'Live intelligence overview aggregated from SentinelX backend agent signals.',
  };
}

async function getVendorSummary(): Promise<VendorRiskDto> {
  const signals = await getSignals('vendor_risk');
  const entities: RiskScore[] = signals.map((signal) => ({
    id: signal.id,
    entity_id: signal.entities[0] ?? signal.id,
    entity_name: signal.entities[0] ?? signal.title,
    score_type: 'vendor_risk',
    score_value: signal.severity * 10,
    risk_level: severityToRiskLevel(signal.severity),
    explanation: signal.summary,
    calculated_at: signal.created_at,
  }));

  return {
    summary:
      signals.length > 0
        ? `Monitoring ${signals.length} vendor risk signal${signals.length === 1 ? '' : 's'} from the backend.`
        : 'No vendor risk signals yet. Run the ingestion pipeline to populate data.',
    entities,
  };
}

async function getAlerts(): Promise<AlertsDto> {
  const signals = await getSignals(undefined, 50);
  const active = signals
    .filter((signal) => signal.severity >= 6)
    .map((signal) => ({
      id: signal.id,
      title: signal.title,
      severity: signal.severity >= 8 ? 'critical' : 'high',
      created_at: signal.created_at,
    }));

  return { active, resolved: [] };
}

async function getCorrelatedEvents(): Promise<CorrelatedEventsDto> {
  try {
    return await get<CorrelatedEvent[]>('/correlation/events');
  } catch {
    return [];
  }
}

async function askRagQuestion(question: string): Promise<RagAnswerDto> {
  try {
    return await post<RagAnswerDto>('/rag/ask', { question });
  } catch (error) {
    const apiError = error as ApiError;
    if (apiError.status === 404 || apiError.status === 502) {
      throw {
        message:
          'RAG service is not available yet. Connect sentinelx-intelligence when Kai Zhe completes the RAG endpoints.',
        status: apiError.status,
      } satisfies ApiError;
    }
    throw error;
  }
}

export const apiClient = {
  get,
  post,
  getHealth: () => get<{ status: string }>('/health'),
  getSignals,
  getDashboardOverview,
  getCyberSignals: (): Promise<ThreatFeedDto> => getSignals('cyber'),
  getGtmSignals: (): Promise<CompetitorIntelligenceDto> => getSignals('gtm'),
  getVendorSignals: () => getSignals('vendor_risk'),
  getVendorSummary,
  getAlerts,
  getCorrelatedEvents,
  getRiskScores: async (): Promise<RiskScore[]> => {
    try {
      return await get<RiskScore[]>('/risk-scores');
    } catch {
      const signals = await getSignals(undefined, 50);
      return signals.map((signal) => ({
        id: signal.id,
        entity_id: signal.entities[0] ?? signal.id,
        entity_name: signal.entities[0] ?? signal.title,
        score_type: signal.signal_type,
        score_value: signal.severity * 10,
        risk_level: severityToRiskLevel(signal.severity),
        explanation: signal.summary,
        calculated_at: signal.created_at,
      }));
    }
  },
  askRagQuestion,
};

export function getApiErrorMessage(error: unknown): string {
  if (error && typeof error === 'object' && 'message' in error) {
    return String((error as ApiError).message);
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'Request failed';
}
