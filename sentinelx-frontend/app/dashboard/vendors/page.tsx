"use client";

import {
  dashboardButtonClass,
  dashboardCardClass,
  dashboardPanelClass,
  PageHeader,
} from '@/components/dashboard/page-header';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { useVendorRisk } from '@/hooks/use-vendor-risk';

export default function VendorsPage() {
  const { loading, error, data, refresh } = useVendorRisk();

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Vendor Monitoring" title="Vendor health and risk intelligence">
        {data?.summary}
      </PageHeader>

      <div className="grid gap-4 lg:grid-cols-2">
        <div className={dashboardPanelClass}>Vendor risk score trend</div>
        <div className={dashboardPanelClass}>Breach and outage history</div>
      </div>

      <div className={dashboardCardClass}>
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-medium text-foreground">Vendor intelligence feed</h3>
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
        ) : data?.entities?.length ? (
          <div className="mt-4 space-y-3">
            {data.entities.map((entity) => (
              <div
                key={entity.id}
                className="flex items-center justify-between rounded-2xl border border-border bg-background px-4 py-4"
              >
                <div>
                  <p className="font-medium text-foreground">{entity.entity_name}</p>
                  <p className="mt-1 text-sm text-muted">{entity.explanation}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm uppercase tracking-[0.2em] text-accent">{entity.risk_level}</p>
                  <p className="mt-1 font-display text-2xl text-foreground">{entity.score_value}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="mt-4 rounded-2xl border border-border bg-background p-5 text-sm text-muted">
            No vendor risk signals yet.
          </p>
        )}
      </div>
    </section>
  );
}
