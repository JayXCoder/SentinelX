"use client";

import { AlertList } from '@/components/dashboard/alert-list';
import { CorrelatedEvents } from '@/components/dashboard/correlated-events';
import { DashboardOverviewPanel } from '@/components/dashboard/dashboard-overview-panel';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { MetricCard } from '@/components/dashboard/metric-card';
import { RiskChart } from '@/components/dashboard/risk-chart';
import { TopEntitiesTable } from '@/components/dashboard/top-entities-table';
import { RealtimeIndicator } from '@/components/dashboard/realtime-indicator';
import { useDashboardOverview } from '@/hooks/use-dashboard-overview';
import { useRealtimeEvents } from '@/hooks/use-realtime-events';
import { apiClient } from '@/lib/api-client';

export default function DashboardPage() {
  useRealtimeEvents();
  const { data, loading, error } = useDashboardOverview();

  if (loading) {
    return <LoadingState label="Loading dashboard overview..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="mx-auto w-full max-w-[1600px] space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 2xl:grid-cols-4">
        <MetricCard label="Intelligence Signals" value={String(data?.intelligence_signals ?? 0)} delta="Live" tone="default" />
        <MetricCard label="Critical Alerts" value={String(data?.critical_alerts ?? 0)} delta="Live" tone="critical" />
        <MetricCard label="Vendor Risks" value={String(data?.vendor_risks ?? 0)} delta="Live" tone="warning" />
        <MetricCard label="Opportunity Score" value={String(data?.opportunity_score ?? 0)} delta="Live" tone="good" />
      </div>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1.65fr)_minmax(0,1fr)]">
        <div className="min-w-0 space-y-6">
          <div className="rounded-[2rem] border border-border bg-[var(--sx-gradient-hero)] p-5 shadow-card sm:p-6 md:p-8">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="min-w-0">
                <p className="text-xs uppercase tracking-[0.35em] text-accent">Executive Overview</p>
                <h2 className="mt-2 font-display text-xl text-foreground sm:text-2xl md:text-3xl">
                  SentinelX intelligence posture
                </h2>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-muted">
                  {data?.summary ??
                    'A premium command center for live threat signals, vendor posture, correlated events, and AI-driven intelligence summaries.'}
                </p>
              </div>
              <RealtimeIndicator />
            </div>
          </div>

          <DashboardOverviewPanel />
          <RiskChart />
          <CorrelatedEvents />
          <TopEntitiesTable />
        </div>

        <div className="min-w-0 space-y-6">
          <div className="rounded-[2rem] border border-border bg-card-solid p-5 shadow-card sm:p-6">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-accent">Live Alerts</p>
                <h3 className="mt-2 text-lg font-medium text-foreground">Critical response queue</h3>
              </div>
              <span className="rounded-full border border-border bg-accent-soft px-3 py-1 text-xs text-muted">
                {data?.critical_alerts ?? 0} active
              </span>
            </div>
            <div className="mt-5">
              <AlertList />
            </div>
          </div>

          <div className="rounded-[2rem] border border-border bg-card-solid p-5 shadow-card sm:p-6">
            <p className="text-sm uppercase tracking-[0.3em] text-muted">System status</p>
            <div className="mt-4 space-y-3 text-sm text-muted">
              <div className="flex flex-wrap items-center justify-between gap-2 rounded-2xl border border-border bg-background px-4 py-3">
                <span>Backend API</span>
                <span className="font-medium text-emerald-700 dark:text-emerald-300">{apiClient.getBackendUrl()}</span>
              </div>
              <div className="flex flex-wrap items-center justify-between gap-2 rounded-2xl border border-border bg-background px-4 py-3">
                <span>Intelligence API</span>
                <span className="font-medium text-emerald-700 dark:text-emerald-300">
                  {apiClient.getIntelligenceUrl()}
                </span>
              </div>
              <div className="flex flex-wrap items-center justify-between gap-2 rounded-2xl border border-border bg-background px-4 py-3">
                <span>Realtime</span>
                <RealtimeIndicator />
              </div>
              <div className="flex flex-wrap items-center justify-between gap-2 rounded-2xl border border-border bg-background px-4 py-3">
                <span>Coverage</span>
                <span className="font-medium text-foreground">Global</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
