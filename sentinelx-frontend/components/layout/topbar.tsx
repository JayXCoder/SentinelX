'use client';

import { Menu, Search, SlidersHorizontal } from 'lucide-react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/theme/theme-toggle';
type TopbarProps = {
  onMenuOpen?: () => void;
};

export function Topbar({ onMenuOpen }: TopbarProps) {
  return (
    <header className="sticky top-0 z-30 flex flex-wrap items-center justify-between gap-3 border-b border-border bg-background/90 px-4 py-3 backdrop-blur-md sm:px-6 sm:py-4">
      <div className="flex min-w-0 flex-1 items-center gap-3">
        <button
          type="button"
          onClick={onMenuOpen}
          className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-border bg-card-solid xl:hidden"
          aria-label="Open menu"
        >
          <Menu className="h-4 w-4" aria-hidden />
        </button>
        <div className="min-w-0">
          <p className="truncate text-xs uppercase tracking-[0.25em] text-accent sm:tracking-[0.3em]">Executive Overview</p>
          <h1 className="truncate font-display text-base text-foreground sm:text-xl md:text-2xl">
            Intelligence Command Center
          </h1>
        </div>
      </div>
      <div className="flex shrink-0 flex-wrap items-center justify-end gap-2">
        <Link href="/" className="hidden text-sm text-muted transition hover:text-foreground lg:inline">
          Home
        </Link>
        <ThemeToggle />
        <button
          type="button"
          className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-border bg-card-solid text-foreground sm:w-auto sm:gap-2 sm:px-4"
          aria-label="Search"
        >
          <Search className="h-4 w-4" aria-hidden />
          <span className="hidden sm:inline text-sm">Search</span>
        </button>
        <button
          type="button"
          className="inline-flex items-center gap-2 rounded-full border border-border bg-card-solid px-3 py-2 text-sm text-foreground sm:px-4"
        >
          <SlidersHorizontal className="h-4 w-4" aria-hidden />
          <span className="hidden sm:inline">Filters</span>
        </button>
      </div>
    </header>
  );
}
