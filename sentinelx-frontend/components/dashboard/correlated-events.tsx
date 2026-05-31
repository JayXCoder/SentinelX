'use client';

import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { useCorrelatedEvents } from '@/hooks/use-correlated-events';

export function CorrelatedEvents() {
  const { data, loading, error } = useCorrelatedEvents(8);

  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 shadow-card">
      <h3 className="font-display text-lg text-foreground">Recent Correlated Events</h3>
      <div className="mt-4 space-y-3 text-sm">
        {loading ? <LoadingState label="Loading correlated events..." /> : null}
        {error ? <ErrorState message={error} /> : null}
        {!loading && !error && data.length === 0 ? (
          <p className="rounded-2xl border border-border bg-background p-4 text-muted">
            No correlated events yet. Run correlation in the intelligence service.
          </p>
        ) : null}
        {!loading && !error
          ? data.map((event) => (
              <div key={event.id} className="rounded-2xl border border-border bg-background p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="font-medium text-foreground">{event.title}</p>
                  <span className="text-xs uppercase tracking-[0.2em] text-accent">{event.event_type}</span>
                </div>
                <p className="mt-2 text-muted">{event.summary}</p>
                <p className="mt-2 text-xs text-muted">{event.correlation_reason}</p>
              </div>
            ))
          : null}
      </div>
    </div>
  );
}
