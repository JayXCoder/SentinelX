"use client";

import { Suspense, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import {
  dashboardButtonClass,
  dashboardCardClass,
  PageHeader,
} from '@/components/dashboard/page-header';
import { ErrorState } from '@/components/dashboard/error-state';
import { FilterBar } from '@/components/dashboard/filter-bar';
import { LoadingState } from '@/components/dashboard/loading-state';
import { PaginationControls } from '@/components/dashboard/pagination-controls';
import { SignalFeed } from '@/components/dashboard/signal-feed';
import { useFilters } from '@/hooks/use-filters';
import { useThreatFeed } from '@/hooks/use-threat-feed';
import { filterSignals } from '@/lib/signal-filters';
import { paginate } from '@/lib/pagination';
import { useDashboardStore } from '@/stores/dashboard-store';

const PAGE_SIZE = 8;

function ThreatFeedContent() {
  const { data, loading, error, refresh } = useThreatFeed();
  const { selectedEntity, selectedRiskLevel, selectedTimeRange } = useFilters();
  const searchQuery = useDashboardStore((state) => state.searchQuery);
  const setSearchQuery = useDashboardStore((state) => state.setSearchQuery);
  const searchParams = useSearchParams();
  const [page, setPage] = useState(1);

  useEffect(() => {
    const query = searchParams.get('q');
    if (query) setSearchQuery(query);
  }, [searchParams, setSearchQuery]);

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
      <PageHeader eyebrow="Threat Feed" title="Live cyber intelligence signals">
        Click any card for sources, story timeline, team notes, and ChamPeng-aware AI analysis.
      </PageHeader>

      <FilterBar />

      <div className={dashboardCardClass}>
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-medium text-foreground">Recent cyber signals</h3>
          <button type="button" onClick={() => void refresh()} className={dashboardButtonClass}>
            Refresh
          </button>
        </div>
        <div className="mt-4 space-y-4">
          {loading ? (
            <LoadingState label="Loading cyber signals..." />
          ) : error ? (
            <ErrorState message={error} />
          ) : (
            <>
              <SignalFeed
                signals={paged.items}
                detailFrom={{ href: '/dashboard/threat-feed', label: 'Threat feed' }}
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

export default function ThreatFeedPage() {
  return (
    <Suspense fallback={<LoadingState label="Loading threat feed..." />}>
      <ThreatFeedContent />
    </Suspense>
  );
}
