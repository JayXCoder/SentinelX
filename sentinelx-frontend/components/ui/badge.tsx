import { cn } from '@/lib/utils';
import type { RiskScore } from '@/types/sentinelx';

const toneByLevel: Record<RiskScore['risk_level'], string> = {
  low: 'bg-emerald-500/15 text-emerald-800 dark:text-emerald-200',
  medium: 'bg-amber-500/15 text-amber-900 dark:text-amber-100',
  high: 'bg-orange-500/15 text-orange-900 dark:text-orange-100',
  critical: 'bg-red-500/15 text-red-900 dark:text-red-100',
};

type BadgeProps = {
  children: React.ReactNode;
  level?: RiskScore['risk_level'];
  className?: string;
};

export function Badge({ children, level, className }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex rounded-full px-2.5 py-1 text-xs font-medium uppercase tracking-[0.15em]',
        level ? toneByLevel[level] : 'bg-accent-soft text-foreground',
        className,
      )}
    >
      {children}
    </span>
  );
}
