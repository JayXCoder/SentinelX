'use client';

import { Badge } from '@/components/ui/badge';
import { DataTable } from '@/components/tables/data-table';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { useTopRisks } from '@/hooks/use-top-risks';
import type { TopRiskDto } from '@/lib/dto';
import type { RiskScore } from '@/types/sentinelx';

export function TopEntitiesTable() {
  const { data, loading, error } = useTopRisks(8);

  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 shadow-card">
      <h3 className="font-display text-lg text-foreground">Top Entities</h3>
      <div className="mt-4">
        {loading ? <LoadingState label="Loading top risks..." /> : null}
        {error ? <ErrorState message={error} /> : null}
        {!loading && !error ? (
          <DataTable<TopRiskDto>
            rows={data}
            rowKey={(row) => row.entity_id}
            emptyMessage="No risk scores ranked yet."
            columns={[
              {
                key: 'entity',
                header: 'Entity',
                render: (row) => <span className="text-foreground">{row.entity_name}</span>,
              },
              {
                key: 'level',
                header: 'Level',
                render: (row) => <Badge level={row.risk_level as RiskScore['risk_level']}>{row.risk_level}</Badge>,
              },
              {
                key: 'score',
                header: 'Score',
                className: 'text-right',
                render: (row) => (
                  <span className="font-medium text-foreground">{Math.round(row.score_value)}</span>
                ),
              },
            ]}
          />
        ) : null}
      </div>
    </div>
  );
}
