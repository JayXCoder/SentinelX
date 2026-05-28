export function LoadingState({ label = 'Loading intelligence data...' }: { label?: string }) {
  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 text-sm text-muted">
      <div className="h-2 w-24 animate-pulse rounded-full bg-accent/60" />
      <p className="mt-4">{label}</p>
    </div>
  );
}
