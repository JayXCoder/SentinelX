import Link from 'next/link';

export function SiteFooter() {
  return (
    <footer className="border-t border-border px-4 py-12 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <p className="max-w-3xl text-xs leading-relaxed text-muted">
          SentinelX provides technology and AI-powered agents for enterprise intelligence, threat monitoring, and risk
          awareness. Platform content is based on customer configuration and pipeline output. By using this site you
          agree to our terms and privacy practices.
        </p>

        <div className="mt-10 flex flex-col gap-6 border-t border-border pt-8 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-2">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[var(--sx-gradient-hero)] text-sm font-semibold">
              S
            </span>
            <span className="font-logo text-lg text-foreground">SentinelX</span>
          </div>

          <nav className="flex flex-wrap gap-6 text-sm text-muted" aria-label="Footer">
            <Link href="/dashboard" className="transition hover:text-foreground">
              Dashboard
            </Link>
            <a href="#faq" className="transition hover:text-foreground">
              FAQ
            </a>
            <span className="text-muted/60">Privacy</span>
            <span className="text-muted/60">Terms</span>
          </nav>
        </div>

        <p className="mt-8 text-xs text-muted">© {new Date().getFullYear()} SentinelX. All rights reserved.</p>
      </div>
    </footer>
  );
}
