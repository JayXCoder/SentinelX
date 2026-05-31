import type { IntelligenceSignal, RiskScore } from '@/types/sentinelx';
import type { TimeRange } from '@/stores/dashboard-store';

const HOURS_BY_RANGE: Record<TimeRange, number> = {
  '24h': 24,
  '7d': 24 * 7,
  '30d': 24 * 30,
};

export function filterSignals(
  signals: IntelligenceSignal[],
  options: {
    searchQuery?: string;
    minSeverity?: number;
    riskLevel?: 'all' | RiskScore['risk_level'];
    entity?: string | null;
    timeRange?: TimeRange;
  },
): IntelligenceSignal[] {
  const query = options.searchQuery?.trim().toLowerCase();
  const hours = options.timeRange ? HOURS_BY_RANGE[options.timeRange] : null;
  const cutoff = hours ? Date.now() - hours * 60 * 60 * 1000 : null;

  return signals.filter((signal) => {
    if (options.minSeverity !== undefined && signal.severity < options.minSeverity) {
      return false;
    }

    if (options.riskLevel && options.riskLevel !== 'all') {
      const level =
        signal.severity >= 8
          ? 'critical'
          : signal.severity >= 6
            ? 'high'
            : signal.severity >= 4
              ? 'medium'
              : 'low';
      if (level !== options.riskLevel) return false;
    }

    if (options.entity) {
      const entity = options.entity.toLowerCase();
      const matchesEntity =
        signal.entities.some((name) => name.toLowerCase().includes(entity)) ||
        signal.title.toLowerCase().includes(entity);
      if (!matchesEntity) return false;
    }

    if (cutoff) {
      const created = new Date(signal.created_at).getTime();
      if (!Number.isNaN(created) && created < cutoff) return false;
    }

    if (query) {
      const haystack = [
        signal.title,
        signal.summary,
        signal.category,
        ...signal.entities,
        ...signal.evidence,
      ]
        .join(' ')
        .toLowerCase();
      if (!haystack.includes(query)) return false;
    }

    return true;
  });
}
