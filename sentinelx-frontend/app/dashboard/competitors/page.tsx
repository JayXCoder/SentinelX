"use client";

import { useEffect, useMemo, useState } from 'react';
import {
  dashboardButtonClass,
  dashboardCardClass,
  PageHeader,
} from '@/components/dashboard/page-header';
import { ErrorState } from '@/components/dashboard/error-state';
import { FilterBar } from '@/components/dashboard/filter-bar';
import { LoadingState } from '@/components/dashboard/loading-state';
import { PaginationControls } from '@/components/dashboard/pagination-controls';
import { ScoreCard } from '@/components/dashboard/score-card';
import { SignalFeed } from '@/components/dashboard/signal-feed';
import { useCompetitorIntelligence } from '@/hooks/use-competitor-intelligence';
import { useFilters } from '@/hooks/use-filters';
import { apiClient } from '@/lib/api-client';
import { filterSignals } from '@/lib/signal-filters';
import { paginate } from '@/lib/pagination';
import { useDashboardStore } from '@/stores/dashboard-store';
import type { RiskScore } from '@/types/sentinelx';

const PAGE_SIZE = 8;

export default function CompetitorsPage() {
  const { data, loading, error, refresh } = useCompetitorIntelligence();
  const { selectedEntity, selectedRiskLevel, selectedTimeRange } = useFilters();
  const searchQuery = useDashboardStore((state) => state.searchQuery);
  const [page, setPage] = useState(1);
  const [opportunities, setOpportunities] = useState<RiskScore[]>([]);

  useEffect(() => {
    void apiClient.getRiskScoresByType('gtm_opportunity').then(setOpportunities).catch(() => setOpportunities([]));
  }, []);

  const filtered = useMemo(
    () =>
      filterSignals(data ?? [], {
        searchQuery,
        entity: selectedEntity,
        riskLevel: selectedRiskLevel,
        timeRange: selectedTimeRange,
      }),
    [data, searchQuery, selectedEntity, selectedRiskLevel, selectedTimeRange],
  );

  const paged = useMemo(() => paginate(filtered, page, PAGE_SIZE), [filtered, page]);

  useEffect(() => {
    setPage(1);
  }, [searchQuery, selectedEntity, selectedRiskLevel, selectedTimeRange]);

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Competitor Intelligence" title="Market movement and opportunity signals">
        GTM signals and opportunity scores from the backend and intelligence risk engine.
      </PageHeader>

      <FilterBar showSeverity={false} />

      {opportunities.length > 0 ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {opportunities.slice(0, 3).map((score) => (
            <ScoreCard key={score.id} score={score} />
          ))}
        </div>
      ) : null}

      <div className={dashboardCardClass}>
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-medium text-foreground">Competitor intelligence feed</h3>
          <button type="button" onClick={() => void refresh()} className={dashboardButtonClass}>
            Refresh
          </button>
        </div>
        <div className="mt-4 space-y-4">
          {loading ? (
            <LoadingState label="Loading competitor intelligence..." />
          ) : error ? (
            <ErrorState message={error} />
          ) : (
            <>
              <SignalFeed
                signals={paged.items}
                detailFrom={{ href: '/dashboard/competitors', label: 'Competitors' }}
              />
              <PaginationControls
                page={paged.page}
                totalPages={paged.totalPages}
                total={paged.total}
                onPageChange={setPage}
              />
            </>
          )}
        </div>
      </div>
    </section>
  );
}
