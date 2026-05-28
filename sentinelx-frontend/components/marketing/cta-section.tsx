'use client';

import { FadeInUp, FloatSlow } from '@/components/marketing/motion';
import { CtaButton } from '@/components/ui/cta-button';

export function CtaSection() {
  return (
    <section className="relative overflow-hidden border-t border-border px-4 py-20 lg:px-8 lg:py-28">
      <FloatSlow className="pointer-events-none absolute -left-20 top-0 h-64 w-64 rounded-full bg-[var(--sx-gradient-hero)] opacity-60 blur-3xl" aria-hidden />
      <div className="pointer-events-none absolute -right-16 bottom-0 h-72 w-72 rounded-full bg-[var(--sx-gradient-hero)] opacity-50 blur-3xl" aria-hidden />

      <FadeInUp className="relative mx-auto max-w-3xl text-center">
        <h2 className="font-display text-4xl tracking-tight text-foreground sm:text-5xl">
          Give a white-glove intelligence experience to every stakeholder
        </h2>
        <p className="mt-5 text-lg text-muted">
          Open the SentinelX dashboard and see how live signals, vendor posture, and exploration come together.
        </p>
        <CtaButton href="/dashboard" variant="warm" size="lg" className="mt-8">
          Let&apos;s explore
        </CtaButton>
      </FadeInUp>
    </section>
  );
}
