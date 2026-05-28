"use client";

import { useAlerts } from '@/hooks/use-alerts';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';

const fallbackAlerts = [
  'Critical cyber signal detected for three entities.',
  'Vendor risk score increased for a strategic supplier.',
  'GTM opportunity surfaced from competitor pricing change.',
];

export function AlertList() {
  const { data, loading, error } = useAlerts();

  if (loading) {
    return <LoadingState label="Loading alerts..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  const alerts = data?.active?.length
    ? data.active.map((alert) => `${alert.title} (${alert.severity})`)
    : fallbackAlerts;

  return (
    <div className="space-y-3 text-sm text-muted">
      {alerts.map((alert) => (
        <div key={alert} className="rounded-2xl border border-border bg-background p-4 text-foreground">
          {alert}
        </div>
      ))}
    </div>
  );
}
