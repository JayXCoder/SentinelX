import type {
  AlertsDto,
  AnalyticsOverviewDto,
  CompetitorIntelligenceDto,
  CorrelatedEventsDto,
  DashboardOverviewDto,
  RagAnswerDto,
  ThreatFeedDto,
  TopRiskDto,
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

type ApiRiskScore = {
  id: string;
  entity_id: string;
  entity_name: string;
  score_type: string;
  score_value: number;
  risk_level: string;
  explanation: string;
  calculated_at: string;
};

type ApiCorrelatedEvent = {
  id: string;
  event_type: string;
  title: string;
  summary: string;
  involved_entities: unknown[];
  signal_ids: unknown[];
  correlation_reason: string;
  confidence: number;
  severity: number;
  first_seen?: string | null;
  last_seen?: string | null;
  created_at?: string;
};

function resolveBackendUrl(): string {
  if (typeof window !== 'undefined') {
    return '/api/backend';
  }
  return (
    process.env.API_BACKEND_URL ??
    process.env.NEXT_PUBLIC_API_BASE_URL ??
    process.env.NEXT_PUBLIC_API_URL ??
    'http://localhost:4000'
  );
}

function resolveIntelligenceUrl(): string {
  if (typeof window !== 'undefined') {
    return '/api/intelligence';
  }
  return (
    process.env.API_INTELLIGENCE_URL ??
    process.env.NEXT_PUBLIC_INTELLIGENCE_API_URL ??
    'http://localhost:4001'
  );
}

const BACKEND_API_URL = resolveBackendUrl();
const INTELLIGENCE_API_URL = resolveIntelligenceUrl();

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

function mapRiskScore(score: ApiRiskScore): RiskScore {
  return {
    id: String(score.id),
    entity_id: String(score.entity_id),
    entity_name: score.entity_name,
    score_type: score.score_type,
    score_value: score.score_value,
    risk_level: score.risk_level as RiskScore['risk_level'],
    explanation: score.explanation,
    calculated_at: score.calculated_at,
  };
}

function mapCorrelatedEvent(event: ApiCorrelatedEvent): CorrelatedEvent {
  const fallbackTime = event.created_at ?? new Date().toISOString();
  return {
    id: String(event.id),
    event_type: event.event_type,
    title: event.title,
    summary: event.summary,
    involved_entities: (event.involved_entities ?? []).map((entity) =>
      typeof entity === 'string' ? entity : JSON.stringify(entity),
    ),
    signal_ids: (event.signal_ids ?? []).map((id) => String(id)),
    correlation_reason: event.correlation_reason,
    confidence: event.confidence,
    severity: event.severity,
    first_seen: event.first_seen ?? fallbackTime,
    last_seen: event.last_seen ?? fallbackTime,
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

async function fetchJson<T>(baseUrl: string, path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${baseUrl}${path}`, {
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

async function backendGet<T>(path: string) {
  return fetchJson<T>(BACKEND_API_URL, path, { method: 'GET' });
}

async function backendPost<T>(path: string, body?: unknown) {
  return fetchJson<T>(BACKEND_API_URL, path, {
    method: 'POST',
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

async function backendPatch<T>(path: string, body?: unknown) {
  return fetchJson<T>(BACKEND_API_URL, path, {
    method: 'PATCH',
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

async function intelligenceGet<T>(path: string) {
  return fetchJson<T>(INTELLIGENCE_API_URL, path, { method: 'GET' });
}

async function intelligencePost<T>(path: string, body?: unknown) {
  return fetchJson<T>(INTELLIGENCE_API_URL, path, {
    method: 'POST',
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

async function getSignals(signalType?: string, limit = 50): Promise<IntelligenceSignal[]> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (signalType) {
    params.set('signal_type', signalType);
  }
  const signals = await backendGet<ApiSignal[]>(`/agents/signals?${params.toString()}`);
  return signals.map(mapSignal);
}

function signalsToRiskScores(signals: IntelligenceSignal[], scoreType?: string): RiskScore[] {
  return signals.map((signal) => ({
    id: signal.id,
    entity_id: signal.entities[0] ?? signal.id,
    entity_name: signal.entities[0] ?? signal.title,
    score_type: scoreType ?? signal.signal_type,
    score_value: signal.severity * 10,
    risk_level: severityToRiskLevel(signal.severity),
    explanation: signal.summary,
    calculated_at: signal.created_at,
  }));
}

async function getDashboardOverview(): Promise<DashboardOverviewDto> {
  try {
    const [analytics, signals] = await Promise.all([
      intelligenceGet<AnalyticsOverviewDto>('/analytics/overview'),
      getSignals(undefined, 100),
    ]);
    const gtmSignals = signals.filter((signal) => signal.signal_type === 'gtm');
    const opportunityScore = gtmSignals.length
      ? Math.round(
          (gtmSignals.reduce((total, signal) => total + signal.confidence, 0) / gtmSignals.length) *
            100,
        )
      : 0;
    const executiveSummary = signals.find((signal) => signal.signal_type === 'executive_summary');

    return {
      intelligence_signals: analytics.total_signals_ingested || signals.length,
      critical_alerts: analytics.critical_risks + analytics.high_risks,
      vendor_risks: analytics.total_risk_scores,
      opportunity_score: opportunityScore,
      correlated_events: analytics.total_correlated_events,
      entities_tracked: analytics.total_entities_tracked,
      summary:
        executiveSummary?.summary ??
        `Tracking ${analytics.total_entities_tracked} entities, ${analytics.total_correlated_events} correlated events, and ${analytics.total_risk_scores} risk scores.`,
    };
  } catch {
    const signals = await getSignals(undefined, 100);
    const criticalAlerts = signals.filter((signal) => signal.severity >= 7).length;
    const vendorRisks = signals.filter((signal) => signal.signal_type === 'vendor_risk').length;
    const gtmSignals = signals.filter((signal) => signal.signal_type === 'gtm');
    const opportunityScore = gtmSignals.length
      ? Math.round(
          (gtmSignals.reduce((total, signal) => total + signal.confidence, 0) / gtmSignals.length) *
            100,
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
}

async function getVendorSummary(): Promise<VendorRiskDto> {
  try {
    const [summary, scores] = await Promise.all([
      intelligenceGet<{
        total_vendors_assessed: number;
        by_risk_level: Record<string, string[]>;
        avg_score: number;
      }>('/analytics/vendor-risk-summary'),
      intelligenceGet<ApiRiskScore[]>('/risk-scores/type/vendor_risk'),
    ]);

    return {
      summary: `Monitoring ${summary.total_vendors_assessed} vendors · average score ${summary.avg_score}.`,
      entities: scores.map(mapRiskScore),
      byRiskLevel: summary.by_risk_level,
    };
  } catch {
    const signals = await getSignals('vendor_risk');
    return {
      summary:
        signals.length > 0
          ? `Monitoring ${signals.length} vendor risk signal${signals.length === 1 ? '' : 's'} from the backend.`
          : 'No vendor risk signals yet. Run the ingestion pipeline to populate data.',
      entities: signalsToRiskScores(signals, 'vendor_risk'),
    };
  }
}

async function getAlerts(): Promise<AlertsDto> {
  const signals = await getSignals(undefined, 50);
  const active = signals
    .filter((signal) => signal.severity >= 6)
    .map((signal) => ({
      id: signal.id,
      title: signal.title,
      severity: (signal.severity >= 8 ? 'critical' : 'high') as 'critical' | 'high',
      created_at: signal.created_at,
      summary: signal.summary,
      signal_type: signal.signal_type,
    }));

  return { active, resolved: [] };
}

async function getCorrelatedEvents(limit = 20): Promise<CorrelatedEventsDto> {
  try {
    const events = await intelligenceGet<ApiCorrelatedEvent[]>(
      `/correlation/events?limit=${limit}`,
    );
    return events.map(mapCorrelatedEvent);
  } catch {
    return [];
  }
}

async function getTopRisks(limit = 10): Promise<TopRiskDto[]> {
  try {
    return await intelligenceGet<TopRiskDto[]>(`/analytics/top-risks?limit=${limit}`);
  } catch {
    const scores = await getRiskScores();
    return scores.slice(0, limit).map((score) => ({
      entity_id: score.entity_id,
      entity_name: score.entity_name,
      score_type: score.score_type,
      score_value: score.score_value,
      risk_level: score.risk_level,
      explanation: score.explanation,
      calculated_at: score.calculated_at,
    }));
  }
}

async function getRiskScores(): Promise<RiskScore[]> {
  try {
    const scores = await intelligenceGet<ApiRiskScore[]>('/risk-scores');
    return scores.map(mapRiskScore);
  } catch {
    const signals = await getSignals(undefined, 50);
    return signalsToRiskScores(signals);
  }
}

async function getRiskScoresByType(scoreType: string): Promise<RiskScore[]> {
  try {
    const scores = await intelligenceGet<ApiRiskScore[]>(`/risk-scores/type/${scoreType}`);
    return scores.map(mapRiskScore);
  } catch {
    const signalType =
      scoreType === 'cyber_exposure'
        ? 'cyber'
        : scoreType === 'vendor_risk'
          ? 'vendor_risk'
          : scoreType === 'gtm_opportunity'
            ? 'gtm'
            : undefined;
    if (!signalType) return [];
    const signals = await getSignals(signalType);
    return signalsToRiskScores(signals, scoreType);
  }
}

async function askRagQuestion(question: string): Promise<RagAnswerDto> {
  return intelligencePost<RagAnswerDto>('/rag/ask', { question });
}

async function askRagWithContext(opts: {
  question: string;
  signalContext?: string;
}): Promise<RagAnswerDto> {
  let workspace_context: string | undefined;
  try {
    const ctx = await backendGet<{ context: string }>('/workspace/context');
    workspace_context = ctx.context;
  } catch {
    workspace_context = undefined;
  }
  return intelligencePost<RagAnswerDto>('/rag/ask', {
    question: opts.question,
    workspace_context,
    signal_context: opts.signalContext,
  });
}

async function getSignalDetail(signalId: string) {
  return backendGet<import('@/types/signal-detail').SignalDetail>(
    `/agents/signals/${signalId}/detail`,
  );
}

async function getWorkspaceProfile() {
  return backendGet<import('@/types/signal-detail').WorkspaceProfile>('/workspace/profile');
}

async function updateWorkspaceProfile(body: {
  company_name?: string;
  profile?: Record<string, unknown>;
}) {
  return backendPatch<import('@/types/signal-detail').WorkspaceProfile>(
    '/workspace/profile',
    body,
  );
}

type ApiSource = {
  id: string;
  name: string;
  source_type: string;
  base_url: string;
  category?: string | null;
  scraping_strategy: string;
  is_active: boolean;
};

async function listSources() {
  return backendGet<ApiSource[]>('/sources');
}

async function createSource(body: {
  name: string;
  source_type: string;
  base_url: string;
  category?: string;
  scraping_strategy?: string;
}) {
  return backendPost<ApiSource>('/sources', body);
}

async function createNote(body: {
  target_type: string;
  target_id: string;
  team_role: string;
  author_name: string;
  content: string;
}) {
  return backendPost<import('@/types/signal-detail').HumanNote>('/notes', body);
}

async function getCyberRiskSummary(): Promise<Record<string, number>> {
  try {
    return await intelligenceGet<Record<string, number>>('/analytics/cyber-risk-summary');
  } catch {
    return {};
  }
}

async function getMarketMovementSummary(): Promise<Record<string, unknown>> {
  try {
    return await intelligenceGet<Record<string, unknown>>('/analytics/market-movement-summary');
  } catch {
    return {};
  }
}

export const apiClient = {
  getBackendUrl: () => BACKEND_API_URL,
  getIntelligenceUrl: () => INTELLIGENCE_API_URL,
  backendGet,
  intelligenceGet,
  backendPost,
  intelligencePost,
  getHealth: () => backendGet<{ status: string }>('/health'),
  getIntelligenceHealth: () => intelligenceGet<{ status: string }>('/health'),
  getSignals,
  getDashboardOverview,
  getCyberSignals: (): Promise<ThreatFeedDto> => getSignals('cyber'),
  getGtmSignals: (): Promise<CompetitorIntelligenceDto> => getSignals('gtm'),
  getVendorSignals: () => getSignals('vendor_risk'),
  getVendorSummary,
  getAlerts,
  getCorrelatedEvents,
  getTopRisks,
  getRiskScores,
  getRiskScoresByType,
  getCyberRiskSummary,
  getMarketMovementSummary,
  askRagQuestion,
  askRagWithContext,
  getSignalDetail,
  getWorkspaceProfile,
  updateWorkspaceProfile,
  listSources,
  createSource,
  createNote,
  getEntityTimeline: (entityId: string) =>
    intelligenceGet<{ entity_id: string; events: unknown[] }>(`/graph/timeline/${entityId}`),
  getGraphEntities: (entityType?: string) => {
    const params = new URLSearchParams({ limit: '50' });
    if (entityType) params.set('entity_type', entityType);
    return intelligenceGet<unknown[]>(`/graph/entities?${params.toString()}`);
  },
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
