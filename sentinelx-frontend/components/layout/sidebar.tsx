import {
  BarChart3,
  Bell,
  LayoutDashboard,
  Radar,
  Settings2,
  ShieldAlert,
  Sparkles,
  Users,
  X,
} from 'lucide-react';
import Link from 'next/link';

const items = [
  { label: 'Overview', icon: LayoutDashboard, href: '/dashboard' },
  { label: 'Threat Feed', icon: ShieldAlert, href: '/dashboard/threat-feed' },
  { label: 'Competitors', icon: Radar, href: '/dashboard/competitors' },
  { label: 'Vendors', icon: Users, href: '/dashboard/vendors' },
  { label: 'Alerts', icon: Bell, href: '/dashboard/alerts' },
  { label: 'Explorer', icon: Sparkles, href: '/dashboard/intelligence-explorer' },
  { label: 'Workspace', icon: Settings2, href: '/dashboard/workspace' },
];

type SidebarProps = {
  onNavigate?: () => void;
};

export function Sidebar({ onNavigate }: SidebarProps) {
  return (
    <div className="flex h-full flex-col px-4 py-6">
      <div className="mb-6 flex items-start justify-between gap-2">
        <div>
          <Link
            href="/"
            onClick={onNavigate}
            className="inline-flex items-center gap-2 rounded-full border border-border bg-accent-soft px-3 py-1 text-xs font-semibold text-accent"
          >
            <BarChart3 className="h-3.5 w-3.5" aria-hidden />
            ChamPeng · SentinelX
          </Link>
          <p className="mt-4 text-sm leading-6 text-muted">
            Monitor OpenAI, Anthropic, Cursor, and Antigravity for your coding-agent platform.
          </p>
        </div>
        {onNavigate ? (
          <button
            type="button"
            onClick={onNavigate}
            className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-border bg-card-solid xl:hidden"
            aria-label="Close navigation"
          >
            <X className="h-4 w-4" aria-hidden />
          </button>
        ) : null}
      </div>

      <nav className="space-y-1 overflow-y-auto" aria-label="Dashboard">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.label}
              href={item.href}
              onClick={onNavigate}
              className="flex items-center gap-3 rounded-2xl px-4 py-3 text-sm text-muted transition hover:bg-accent-soft hover:text-foreground"
            >
              <Icon className="h-4 w-4 shrink-0 text-accent" aria-hidden />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
