'use client';

import { useState } from 'react';
import { cn } from '@/lib/utils';
import { Sidebar } from './sidebar';
import { Topbar } from './topbar';

export function DashboardShell({ children }: Readonly<{ children: React.ReactNode }>) {
  const [mobileNavOpen, setMobileNavOpen] = useState(false);

  return (
    <div className="flex min-h-dvh w-full overflow-x-hidden">
      {mobileNavOpen ? (
        <button
          type="button"
          aria-label="Close menu"
          className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm xl:hidden"
          onClick={() => setMobileNavOpen(false)}
        />
      ) : null}

      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-[min(100vw,18rem)] shrink-0 border-r border-border bg-elevated transition-transform duration-300 ease-out xl:static xl:z-auto xl:translate-x-0',
          mobileNavOpen ? 'translate-x-0' : '-translate-x-full xl:translate-x-0',
        )}
      >
        <Sidebar onNavigate={() => setMobileNavOpen(false)} />
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar onMenuOpen={() => setMobileNavOpen(true)} />
        <main className="min-w-0 flex-1 px-4 py-4 sm:px-6 sm:py-6">{children}</main>
      </div>
    </div>
  );
}
