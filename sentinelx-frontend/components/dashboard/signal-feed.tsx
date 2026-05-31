'use client';

import { useRouter } from 'next/navigation';
import type { IntelligenceSignal } from '@/types/sentinelx';

type SignalFeedProps = {
  signals?: IntelligenceSignal[];
  onSelect?: (signal: IntelligenceSignal) => void;
  detailFrom?: { href: string; label: string };
};

export function SignalFeed({ signals, onSelect, detailFrom }: SignalFeedProps) {
  const router = useRouter();
  if (!signals?.length) {
    return (
      <p className="rounded-2xl border border-border bg-background p-5 text-sm text-muted">
        No signals match the current filters.
      </p>
    );
  }

  return (
    <div className="space-y-3">
      {signals.map((signal) => (
        <button
          key={signal.id}
          type="button"
          onClick={() => {
            if (onSelect) {
              onSelect(signal);
              return;
            }
            if (detailFrom) {
              const q = new URLSearchParams({
                from: detailFrom.href,
                fromLabel: detailFrom.label,
              });
              router.push(`/dashboard/signals/${signal.id}?${q.toString()}`);
            }
          }}
          className="w-full rounded-2xl border border-border bg-card-solid p-4 text-left transition hover:border-accent/30 hover:bg-accent-soft/50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
        >
          <p className="text-sm text-foreground">{signal.title}</p>
          <p className="mt-1 text-xs uppercase tracking-[0.2em] text-muted">
            {signal.category} · Severity {signal.severity}
          </p>
          <p className="mt-2 line-clamp-2 text-sm leading-6 text-muted">{signal.summary}</p>
          {detailFrom ? (
            <p className="mt-2 text-xs font-medium text-accent">View full detail & sources →</p>
          ) : null}
        </button>
      ))}
    </div>
  );
}
