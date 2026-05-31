"use client";

import Link from 'next/link';
import { useRouter } from 'next/navigation';
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
import { useVendorRisk } from '@/hooks/use-vendor-risk';
import { apiClient } from '@/lib/api-client';
import { useFilters } from '@/hooks/use-filters';
import { paginate } from '@/lib/pagination';
import { useDashboardStore } from '@/stores/dashboard-store';
const PAGE_SIZE = 6;

export default function VendorsPage() {
  const router = useRouter();
  const { loading, error, data, refresh } = useVendorRisk();
  const { selectedRiskLevel } = useFilters();
  const searchQuery = useDashboardStore((state) => state.searchQuery);
  const [page, setPage] = useState(1);
  const [vendorSignals, setVendorSignals] = useState<Record<string, string>>({});

  useEffect(() => {
    void apiClient.getVendorSignals().then((signals) => {
      const map: Record<string, string> = {};
      for (const s of signals) {
        for (const e of s.entities) {
          map[e] = s.id;
        }
      }
      setVendorSignals(map);
    });
  }, []);

  const filtered = useMemo(() => {
    const entities = data?.entities ?? [];
    return entities.filter((entity) => {
      if (selectedRiskLevel !== 'all' && entity.risk_level !== selectedRiskLevel) return false;
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        return (
          entity.entity_name.toLowerCase().includes(query) ||
          entity.explanation.toLowerCase().includes(query)
        );
      }
      return true;
    });
  }, [data?.entities, selectedRiskLevel, searchQuery]);

  const paged = useMemo(() => paginate(filtered, page, PAGE_SIZE), [filtered, page]);

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Vendor Monitoring" title="Vendor health and risk intelligence">
        {data?.summary}
      </PageHeader>

      <FilterBar showEntity />

      <div className={dashboardCardClass}>
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-medium text-foreground">Vendor risk scores</h3>
          <button type="button" onClick={() => void refresh()} className={dashboardButtonClass}>
            Refresh
          </button>
        </div>
        {loading ? (
          <div className="mt-4">
            <LoadingState label="Loading vendor intelligence..." />
          </div>
        ) : error ? (
          <div className="mt-4">
            <ErrorState message={error} />
          </div>
        ) : paged.total > 0 ? (
          <div className="mt-4 space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              {paged.items.map((entity) => (
                <ScoreCard
                  key={entity.id}
                  score={entity}
                  onSelect={(score) => {
                    const signalId = vendorSignals[score.entity_name];
                    if (signalId) {
                      router.push(
                        `/dashboard/signals/${signalId}?from=${encodeURIComponent('/dashboard/vendors')}&fromLabel=${encodeURIComponent('Vendors')}`,
                      );
                    }
                  }}
                />
              ))}
            </div>
            <PaginationControls
              page={paged.page}
              totalPages={paged.totalPages}
              total={paged.total}
              onPageChange={setPage}
            />
          </div>
        ) : (
          <p className="mt-4 rounded-2xl border border-border bg-background p-5 text-sm text-muted">
            No vendor risk scores yet.
          </p>
        )}
      </div>

      <p className="text-sm text-muted">
        Click a vendor card to open linked intelligence with sources and AI. Or{' '}
        <Link href="/dashboard/workspace" className="text-accent hover:underline">
          manage sources in Workspace
        </Link>
        .
      </p>
    </section>
  );
}
