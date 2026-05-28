export function RiskChart() {
  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 shadow-card">
      <h3 className="font-display text-lg text-foreground">Risk Overview</h3>
      <div className="mt-6 flex h-44 items-end gap-3">
        {[38, 52, 44, 68, 58, 74, 82].map((height, index) => (
          <div
            key={index}
            className="flex-1 rounded-t-2xl bg-gradient-to-t from-accent to-[#c97bd8]"
            style={{ height: `${height}%` }}
          />
        ))}
      </div>
    </div>
  );
}
