const entities = [
  ['Acme Corp', 'Critical', '92'],
  ['Northwind', 'High', '84'],
  ['Globex', 'Medium', '67'],
];

export function TopEntitiesTable() {
  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 shadow-card">
      <h3 className="font-display text-lg text-foreground">Top Entities</h3>
      <div className="mt-4 space-y-3 text-sm">
        {entities.map(([name, level, score]) => (
          <div
            key={name}
            className="flex items-center justify-between rounded-2xl border border-border bg-background px-4 py-3 text-muted"
          >
            <span className="text-foreground">{name}</span>
            <span>{level}</span>
            <span className="font-medium text-foreground">{score}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
