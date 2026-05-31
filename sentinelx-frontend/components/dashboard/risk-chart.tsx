'use client';

import { useEffect, useState } from 'react';
import { apiClient } from '@/lib/api-client';

type ChartBar = {
  label: string;
  value: number;
};

export function RiskChart() {
  const [bars, setBars] = useState<ChartBar[]>([]);

  useEffect(() => {
    void apiClient.getRiskScores().then((scores) => {
      const grouped = scores.reduce<Record<string, number>>((acc, score) => {
        acc[score.risk_level] = (acc[score.risk_level] ?? 0) + score.score_value;
        return acc;
      }, {});

      const nextBars: ChartBar[] = ['critical', 'high', 'medium', 'low'].map((level) => ({
        label: level,
        value: grouped[level] ?? 0,
      }));

      setBars(nextBars.some((bar) => bar.value > 0) ? nextBars : []);
    });
  }, []);

  const maxValue = Math.max(...bars.map((bar) => bar.value), 1);

  return (
    <div className="rounded-3xl border border-border bg-card-solid p-6 shadow-card">
      <h3 className="font-display text-lg text-foreground">Risk Overview</h3>
      {bars.length === 0 ? (
        <p className="mt-6 text-sm text-muted">No risk scores available yet.</p>
      ) : (
        <div className="mt-6 flex h-44 items-end gap-3">
          {bars.map((bar) => (
            <div key={bar.label} className="flex flex-1 flex-col items-center gap-2">
              <div
                className="w-full rounded-t-2xl bg-gradient-to-t from-accent to-[#c97bd8] transition-all duration-500"
                style={{ height: `${Math.max(12, (bar.value / maxValue) * 100)}%` }}
                title={`${bar.label}: ${Math.round(bar.value)}`}
              />
              <span className="text-xs uppercase tracking-[0.15em] text-muted">{bar.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
