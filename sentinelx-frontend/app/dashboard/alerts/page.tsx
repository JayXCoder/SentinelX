"use client";

import { dashboardButtonClass, dashboardCardClass, PageHeader } from '@/components/dashboard/page-header';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { useAlerts } from '@/hooks/use-alerts';

export default function AlertsPage() {
  const { data, loading, error, refresh } = useAlerts();

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Alerts" title="Notification visibility and response">
        High-severity intelligence signals surfaced from the SentinelX backend.
      </PageHeader>

      <div className={dashboardCardClass}>
        <div className="flex items-center justify-between gap-4">
          <h3 className="text-lg font-medium text-foreground">Active alerts</h3>
          <button type="button" onClick={() => void refresh()} className={dashboardButtonClass}>
            Refresh
          </button>
        </div>
        {loading ? (
          <div className="mt-4">
            <LoadingState label="Loading alerts..." />
          </div>
        ) : error ? (
          <div className="mt-4">
            <ErrorState message={error} />
          </div>
        ) : data?.active?.length ? (
          <div className="mt-4 space-y-3">
            {data.active.map((alert) => (
              <div key={alert.id} className="rounded-2xl border border-border bg-background p-5">
                <div className="flex items-center justify-between gap-4">
                  <p className="font-medium text-foreground">{alert.title}</p>
                  <span className="rounded-full border border-rose-500/25 bg-rose-500/10 px-3 py-1 text-xs text-rose-800 dark:text-rose-200">
                    {alert.severity}
                  </span>
                </div>
                <p className="mt-2 text-xs text-muted">{new Date(alert.created_at).toLocaleString()}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="mt-4 rounded-2xl border border-border bg-background p-5 text-sm text-muted">
            No active alerts. Alerts appear when signal severity is 6 or higher.
          </p>
        )}
      </div>
    </section>
  );
}
