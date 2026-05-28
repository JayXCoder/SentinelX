"use client";

import {
  dashboardButtonClass,
  dashboardCardClass,
  dashboardPanelClass,
  PageHeader,
} from '@/components/dashboard/page-header';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { SignalFeed } from '@/components/dashboard/signal-feed';
import { useThreatFeed } from '@/hooks/use-threat-feed';

export default function ThreatFeedPage() {
  const { loading, error, data, refresh } = useThreatFeed();

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Threat Feed" title="Live cyber intelligence signals">
        Monitor CVEs, breach mentions, phishing indicators, and high-severity cyber events from{' '}
        <code className="text-accent">/agents/signals?signal_type=cyber</code>.
      </PageHeader>

      <div className="grid gap-4 lg:grid-cols-3">
        <div className={dashboardPanelClass}>Severity filters</div>
        <div className={dashboardPanelClass}>Keyword search</div>
        <div className={dashboardPanelClass}>Entity targeting</div>
      </div>

      <div className={dashboardCardClass}>
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-medium text-foreground">Recent cyber signals</h3>
          <button type="button" onClick={() => void refresh()} className={dashboardButtonClass}>
            Refresh
          </button>
        </div>
        <div className="mt-4">
          {loading ? (
            <LoadingState label="Loading cyber signals..." />
          ) : error ? (
            <ErrorState message={error} />
          ) : data?.length ? (
            <SignalFeed signals={data} />
          ) : (
            <p className="rounded-2xl border border-border bg-background p-5 text-sm text-muted">
              No cyber signals yet. Run the backend ingestion pipeline to populate intelligence data.
            </p>
          )}
        </div>
      </div>
    </section>
  );
}
