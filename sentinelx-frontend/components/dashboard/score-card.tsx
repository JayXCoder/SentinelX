import { Badge } from '@/components/ui/badge';
import type { RiskScore } from '@/types/sentinelx';
import { cn } from '@/lib/utils';

type ScoreCardProps = {
  score: RiskScore;
  onSelect?: (score: RiskScore) => void;
  className?: string;
};

export function ScoreCard({ score, onSelect, className }: ScoreCardProps) {
  const content = (
    <>
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate font-medium text-foreground">{score.entity_name}</p>
          <p className="mt-1 text-xs uppercase tracking-[0.2em] text-muted">{score.score_type}</p>
        </div>
        <Badge level={score.risk_level}>{score.risk_level}</Badge>
      </div>
      <p className="mt-4 font-display text-3xl text-foreground">{Math.round(score.score_value)}</p>
      <p className="mt-2 line-clamp-3 text-sm leading-6 text-muted">{score.explanation}</p>
    </>
  );

  if (onSelect) {
    return (
      <button
        type="button"
        onClick={() => onSelect(score)}
        className={cn(
          'w-full rounded-2xl border border-border bg-background p-4 text-left transition hover:border-accent/40 hover:bg-accent-soft/30 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent',
          className,
        )}
      >
        {content}
      </button>
    );
  }

  return (
    <div className={cn('rounded-2xl border border-border bg-background p-4', className)}>{content}</div>
  );
}
