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
import { useCompetitorIntelligence } from '@/hooks/use-competitor-intelligence';

export default function CompetitorsPage() {
  const { data, loading, error, refresh } = useCompetitorIntelligence();

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Competitor Intelligence" title="Market movement and opportunity signals">
        GTM signals from <code className="text-accent">/agents/signals?signal_type=gtm</code>.
      </PageHeader>

      <div className="grid gap-4 md:grid-cols-3">
        <div className={dashboardPanelClass}>Competitor filter</div>
        <div className={dashboardPanelClass}>Signal type filter</div>
        <div className={dashboardPanelClass}>Opportunity score</div>
      </div>

      <div className={dashboardCardClass}>
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-medium text-foreground">Competitor intelligence feed</h3>
          <button type="button" onClick={() => void refresh()} className={dashboardButtonClass}>
            Refresh
          </button>
        </div>
        <div className="mt-4">
          {loading ? (
            <LoadingState label="Loading competitor intelligence..." />
          ) : error ? (
            <ErrorState message={error} />
          ) : data?.length ? (
            <SignalFeed signals={data} />
          ) : (
            <p className="rounded-2xl border border-border bg-background p-5 text-sm text-muted">No GTM signals yet.</p>
          )}
        </div>
      </div>
    </section>
  );
}
