const events = [
  'Identity exposure correlated with vendor signal cluster.',
  'Threat activity matched competitor infrastructure change.',
  'Vendor outage linked with correlated alert spike.',
];

export function CorrelatedEvents() {
  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 shadow-card">
      <h3 className="font-display text-lg text-foreground">Recent Correlated Events</h3>
      <div className="mt-4 space-y-3 text-sm text-muted">
        {events.map((event) => (
          <div key={event} className="rounded-2xl border border-border bg-background p-4 text-foreground">
            {event}
          </div>
        ))}
      </div>
    </div>
  );
}
