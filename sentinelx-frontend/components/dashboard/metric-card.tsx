type MetricCardProps = {
  label: string;
  value: string;
  delta?: string;
  tone?: 'default' | 'good' | 'warning' | 'critical';
};

export function MetricCard({ label, value, delta, tone = 'default' }: MetricCardProps) {
  const toneClasses = {
    default: 'border-border bg-card-solid',
    good: 'border-emerald-500/25 bg-emerald-500/10',
    warning: 'border-amber-500/25 bg-amber-500/10',
    critical: 'border-rose-500/25 bg-rose-500/10',
  };

  return (
    <div
      className={`rounded-3xl border p-5 shadow-card transition hover:-translate-y-0.5 hover:shadow-soft ${toneClasses[tone]}`}
    >
      <p className="text-sm text-muted">{label}</p>
      <div className="mt-2 flex items-end justify-between gap-4">
        <p className="font-display text-3xl tracking-tight text-foreground">{value}</p>
        {delta ? <span className="text-sm text-accent">{delta}</span> : null}
      </div>
    </div>
  );
}
