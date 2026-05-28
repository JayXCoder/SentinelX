'use client';

import { motion } from 'framer-motion';
import { CtaButton } from '@/components/ui/cta-button';

const orbs = [
  { size: 'h-24 w-24', top: '8%', left: '6%', delay: 0 },
  { size: 'h-16 w-16', top: '18%', right: '12%', delay: 0.15 },
  { size: 'h-20 w-20', bottom: '22%', left: '4%', delay: 0.25 },
  { size: 'h-14 w-14', bottom: '12%', right: '8%', delay: 0.35 },
  { size: 'h-28 w-28', top: '42%', right: '2%', delay: 0.2 },
];

const feedItems = [
  { label: 'CVE exposure cluster', time: '2m ago', tone: 'critical' },
  { label: 'Vendor outage signal', time: '8m ago', tone: 'warning' },
  { label: 'Competitor pricing shift', time: '14m ago', tone: 'info' },
];

export function DemoShowcase() {
  return (
    <div className="relative mx-auto w-full max-w-lg">
      {orbs.map((orb, index) => (
        <motion.div
          key={index}
          className={`pointer-events-none absolute rounded-full bg-[var(--sx-gradient-hero)] blur-2xl ${orb.size}`}
          style={{ top: orb.top, left: orb.left, right: orb.right, bottom: orb.bottom }}
          animate={{ y: [0, -12, 0], scale: [1, 1.05, 1], opacity: [0.5, 0.9, 0.5] }}
          transition={{ duration: 5 + index * 0.5, repeat: Infinity, delay: orb.delay, ease: 'easeInOut' }}
          aria-hidden
        />
      ))}

      <motion.div
        className="relative overflow-hidden rounded-3xl border border-border bg-card-solid p-1 shadow-soft"
        whileHover={{ scale: 1.01 }}
        transition={{ type: 'spring', stiffness: 300, damping: 24 }}
      >
        <div className="rounded-[1.35rem] bg-[var(--sx-gradient-hero)] p-6 sm:p-8">
          <div className="flex items-center justify-between">
            <span className="rounded-full bg-card-solid/90 px-3 py-1 text-xs font-medium text-foreground backdrop-blur">
              Intelligence demo
            </span>
            <span className="flex items-center gap-1.5 text-xs font-medium text-foreground/80">
              <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
              Live
            </span>
          </div>

          <div className="mt-6 space-y-2.5 rounded-2xl border border-border/60 bg-card-solid/95 p-4 backdrop-blur">
            {feedItems.map((item, i) => (
              <motion.div
                key={item.label}
                initial={{ opacity: 0, x: 12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.12, duration: 0.4 }}
                className="flex items-center justify-between gap-3 rounded-xl border border-border bg-background/60 px-3 py-3"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <span
                    className={`h-2 w-2 shrink-0 rounded-full ${
                      item.tone === 'critical'
                        ? 'bg-rose-500'
                        : item.tone === 'warning'
                          ? 'bg-amber-500'
                          : 'bg-sky-500'
                    }`}
                  />
                  <span className="truncate text-sm text-foreground">{item.label}</span>
                </div>
                <span className="shrink-0 text-xs text-muted">{item.time}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      <div className="mt-8 text-center">
        <p className="text-sm font-medium text-muted">See SentinelX in action</p>
        <h2 className="mt-1 font-display text-2xl text-foreground">Live intelligence feed</h2>
        <p className="mt-2 text-sm text-muted">Walk through threats, vendors, and GTM signals in one view.</p>
        <CtaButton href="/dashboard" variant="secondary" className="mt-5">
          Start demo
        </CtaButton>
      </div>
    </div>
  );
}
