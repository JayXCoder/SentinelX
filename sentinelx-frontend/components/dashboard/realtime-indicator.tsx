'use client';

import { useDashboardStore } from '@/stores/dashboard-store';
import { cn } from '@/lib/utils';

const toneStyles = {
  connected: 'border-emerald-500/25 bg-emerald-500/15 text-emerald-800 dark:text-emerald-200',
  polling: 'border-amber-500/25 bg-amber-500/15 text-amber-900 dark:text-amber-100',
  offline: 'border-border bg-background text-muted',
} as const;

export function RealtimeIndicator() {
  const status = useDashboardStore((state) => state.realtimeStatus);

  const label =
    status === 'connected'
      ? 'Live WebSocket'
      : status === 'polling'
        ? 'Polling (30s)'
        : 'Offline';

  return (
    <span
      className={cn(
        'inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium',
        toneStyles[status],
      )}
      role="status"
      aria-live="polite"
    >
      <span
        className={cn(
          'h-2 w-2 rounded-full',
          status === 'connected' && 'bg-emerald-500 animate-pulse',
          status === 'polling' && 'bg-amber-500',
          status === 'offline' && 'bg-muted',
        )}
        aria-hidden
      />
      {label}
    </span>
  );
}
