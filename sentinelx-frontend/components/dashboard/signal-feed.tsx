import type { IntelligenceSignal } from '@/types/sentinelx';

const fallbackSignals = [
  { title: 'CVE-linked exposure detected', meta: 'Cyber · High' },
  { title: 'Competitor pricing shift observed', meta: 'GTM · Opportunity' },
  { title: 'Vendor incident mentions increased', meta: 'Vendor · Medium' },
];

type SignalFeedProps = {
  signals?: IntelligenceSignal[];
};

export function SignalFeed({ signals }: SignalFeedProps) {
  if (signals?.length) {
    return (
      <div className="space-y-3">
        {signals.map((signal) => (
          <div
            key={signal.id}
            className="rounded-2xl border border-border bg-card-solid p-4 transition hover:border-accent/30 hover:bg-accent-soft/50"
          >
            <p className="text-sm text-foreground">{signal.title}</p>
            <p className="mt-1 text-xs uppercase tracking-[0.2em] text-muted">
              {signal.category} · Severity {signal.severity}
            </p>
            <p className="mt-2 text-sm leading-6 text-muted">{signal.summary}</p>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {fallbackSignals.map((signal) => (
        <div
          key={signal.title}
          className="rounded-2xl border border-border bg-card-solid p-4 transition hover:border-accent/30"
        >
          <p className="text-sm text-foreground">{signal.title}</p>
          <p className="mt-1 text-xs uppercase tracking-[0.2em] text-muted">{signal.meta}</p>
        </div>
      ))}
    </div>
  );
}
