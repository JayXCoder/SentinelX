"use client";

import { useDashboardOverview } from '@/hooks/use-dashboard-overview';
import type { DashboardOverviewDto } from '@/lib/dto';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';

export function DashboardOverviewPanel() {
  const { data, loading, error } = useDashboardOverview();
  const overview = data as DashboardOverviewDto | null;

  if (loading) {
    return <LoadingState label="Loading dashboard overview..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 shadow-card">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="font-display text-xl text-foreground">Dashboard Overview</h2>
          <p className="mt-2 text-sm text-muted">{overview?.summary ?? 'Executive intelligence snapshot.'}</p>
        </div>
        <span className="rounded-full border border-border bg-accent-soft px-3 py-1 text-xs text-accent">Live</span>
      </div>
      <div className="mt-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <Stat label="Signals" value={String(overview?.intelligence_signals ?? 0)} />
        <Stat label="Critical" value={String(overview?.critical_alerts ?? 0)} />
        <Stat label="Vendor risks" value={String(overview?.vendor_risks ?? 0)} />
        <Stat label="Opportunity" value={String(overview?.opportunity_score ?? 0)} />
      </div>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-border bg-background p-4">
      <p className="text-sm text-muted">{label}</p>
      <p className="mt-2 font-display text-2xl text-foreground">{value}</p>
    </div>
  );
}
