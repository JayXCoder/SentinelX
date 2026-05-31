'use client';

import { useState } from 'react';
import { Menu, Search, SlidersHorizontal } from 'lucide-react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/theme/theme-toggle';
import { RealtimeIndicator } from '@/components/dashboard/realtime-indicator';
import { SearchDialog } from '@/components/dashboard/search-dialog';
import { useDashboardStore } from '@/stores/dashboard-store';

type TopbarProps = {
  onMenuOpen?: () => void;
};

export function Topbar({ onMenuOpen }: TopbarProps) {
  const [searchOpen, setSearchOpen] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const setSelectedRiskLevel = useDashboardStore((state) => state.setSelectedRiskLevel);

  return (
    <>
      <header className="sticky top-0 z-30 flex flex-wrap items-center justify-between gap-3 border-b border-border bg-background/90 px-4 py-3 backdrop-blur-md sm:px-6 sm:py-4">
        <div className="flex min-w-0 flex-1 items-center gap-3">
          <button
            type="button"
            onClick={onMenuOpen}
            className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-border bg-card-solid xl:hidden focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
            aria-label="Open menu"
          >
            <Menu className="h-4 w-4" aria-hidden />
          </button>
          <div className="min-w-0">
            <p className="truncate text-xs uppercase tracking-[0.25em] text-accent sm:tracking-[0.3em]">
              ChamPeng · SentinelX
            </p>
            <h1 className="truncate font-display text-base text-foreground sm:text-xl md:text-2xl">
              Competitive intelligence command center
            </h1>
          </div>
        </div>
        <div className="flex shrink-0 flex-wrap items-center justify-end gap-2">
          <RealtimeIndicator />
          <Link
            href="/"
            className="hidden text-sm text-muted transition hover:text-foreground focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent lg:inline"
          >
            Home
          </Link>
          <ThemeToggle />
          <button
            type="button"
            onClick={() => setSearchOpen(true)}
            className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border bg-card-solid text-foreground sm:w-auto sm:gap-2 sm:px-4 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
            aria-label="Search intelligence"
          >
            <Search className="h-4 w-4" aria-hidden />
            <span className="hidden sm:inline text-sm">Search</span>
          </button>
          <button
            type="button"
            onClick={() => setFiltersOpen((open) => !open)}
            aria-expanded={filtersOpen}
            className="inline-flex items-center gap-2 rounded-full border border-border bg-card-solid px-3 py-2 text-sm text-foreground sm:px-4 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
          >
            <SlidersHorizontal className="h-4 w-4" aria-hidden />
            <span className="hidden sm:inline">Filters</span>
          </button>
        </div>
        {filtersOpen ? (
          <div className="w-full border-t border-border pt-3">
            <label className="block text-sm">
              <span className="text-xs uppercase tracking-[0.2em] text-muted">Quick risk filter</span>
              <select
                className="mt-2 w-full rounded-2xl border border-border bg-card-solid px-3 py-2 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent"
                defaultValue="all"
                onChange={(event) =>
                  setSelectedRiskLevel(event.target.value as 'all' | 'low' | 'medium' | 'high' | 'critical')
                }
              >
                <option value="all">All levels</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </label>
          </div>
        ) : null}
      </header>
      <SearchDialog open={searchOpen} onClose={() => setSearchOpen(false)} />
    </>
  );
}
