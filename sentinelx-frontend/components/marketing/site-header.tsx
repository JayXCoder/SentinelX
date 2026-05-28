import Link from 'next/link';
import { ThemeToggle } from '@/components/theme/theme-toggle';
import { CtaButton } from '@/components/ui/cta-button';

const nav = [
  { label: 'Capabilities', href: '#capabilities' },
  { label: 'How it works', href: '#how-it-works' },
  { label: 'Platform', href: '#platform' },
  { label: 'FAQ', href: '#faq' },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 lg:px-8">
        <Link href="/" className="flex items-center gap-2.5">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[var(--sx-gradient-hero)] font-logo text-base text-foreground shadow-card">
            S
          </span>
          <span className="font-logo text-xl text-foreground">SentinelX</span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex" aria-label="Primary">
          {nav.map((item) => (
            <a
              key={item.label}
              href={item.href}
              className="text-sm text-muted transition hover:text-foreground"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2 sm:gap-3">
          <ThemeToggle />
          <CtaButton href="/dashboard" variant="ghost" className="hidden sm:inline-flex">
            Sign in
          </CtaButton>
          <CtaButton href="/dashboard" variant="solid" size="sm">
            Get started
          </CtaButton>
        </div>
      </div>
    </header>
  );
}
