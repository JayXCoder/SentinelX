'use client';

import { useFilters } from '@/hooks/use-filters';
import { useDashboardStore } from '@/stores/dashboard-store';
import { cn } from '@/lib/utils';

type FilterBarProps = {
  showSeverity?: boolean;
  showEntity?: boolean;
  className?: string;
};

const riskLevels = ['all', 'low', 'medium', 'high', 'critical'] as const;
const timeRanges = ['24h', '7d', '30d'] as const;

export function FilterBar({ showSeverity = true, showEntity = true, className }: FilterBarProps) {
  const { selectedEntity, selectedRiskLevel, selectedTimeRange, setSelectedEntity, setSelectedRiskLevel, setSelectedTimeRange } =
    useFilters();
  const searchQuery = useDashboardStore((state) => state.searchQuery);
  const setSearchQuery = useDashboardStore((state) => state.setSearchQuery);

  return (
    <div className={cn('grid gap-4 lg:grid-cols-3', className)}>
      {showSeverity ? (
        <label className="rounded-2xl border border-border bg-background px-4 py-3 text-sm">
          <span className="text-xs uppercase tracking-[0.2em] text-muted">Risk level</span>
          <select
            value={selectedRiskLevel}
            onChange={(event) =>
              setSelectedRiskLevel(event.target.value as typeof selectedRiskLevel)
            }
            className="mt-2 w-full bg-transparent text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
          >
            {riskLevels.map((level) => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>
        </label>
      ) : null}

      <label className="rounded-2xl border border-border bg-background px-4 py-3 text-sm">
        <span className="text-xs uppercase tracking-[0.2em] text-muted">Time range</span>
        <select
          value={selectedTimeRange}
          onChange={(event) => setSelectedTimeRange(event.target.value as typeof selectedTimeRange)}
          className="mt-2 w-full bg-transparent text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
        >
          {timeRanges.map((range) => (
            <option key={range} value={range}>
              {range}
            </option>
          ))}
        </select>
      </label>

      {showEntity ? (
        <label className="rounded-2xl border border-border bg-background px-4 py-3 text-sm">
          <span className="text-xs uppercase tracking-[0.2em] text-muted">Entity / keyword</span>
          <input
            value={searchQuery || selectedEntity || ''}
            onChange={(event) => {
              setSearchQuery(event.target.value);
              setSelectedEntity(event.target.value || null);
            }}
            placeholder="Filter by entity or keyword"
            className="mt-2 w-full bg-transparent text-foreground placeholder:text-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
          />
        </label>
      ) : null}
    </div>
  );
}
