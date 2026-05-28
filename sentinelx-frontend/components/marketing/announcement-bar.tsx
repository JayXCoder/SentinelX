import { ArrowUpRight } from 'lucide-react';
import Link from 'next/link';

export function AnnouncementBar() {
  return (
    <div className="border-b border-border bg-[var(--sx-announcement)]">
      <div className="mx-auto flex max-w-6xl items-center justify-center px-4 py-2.5 text-center">
        <Link
          href="/dashboard"
          className="group inline-flex flex-wrap items-center justify-center gap-1 text-sm text-muted transition hover:text-foreground"
        >
          <span>SentinelX intelligence pipeline is live — explore the dashboard.</span>
          <span className="font-medium text-foreground underline-offset-4 group-hover:underline">
            Open dashboard
          </span>
          <ArrowUpRight className="h-3.5 w-3.5 text-accent transition group-hover:translate-x-0.5 group-hover:-translate-y-0.5" aria-hidden />
        </Link>
      </div>
    </div>
  );
}
