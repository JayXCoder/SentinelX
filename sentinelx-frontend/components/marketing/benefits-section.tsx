'use client';

import { FadeInUp, StaggerItem, StaggerReveal } from '@/components/marketing/motion';

const benefits = [
  {
    title: 'Live 24/7',
    body: 'Always available to surface new intelligence signals.',
  },
  {
    title: 'Multi-domain',
    body: 'Cyber, GTM, vendor, financial, and OSINT in one platform.',
  },
  {
    title: 'Tailored per entity',
    body: 'Adapts scoring and summaries to the entities you care about.',
  },
];

export function BenefitsSection() {
  return (
    <section className="border-t border-border px-4 py-20 lg:px-8 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <FadeInUp>
          <h2 className="font-display text-4xl tracking-tight text-foreground sm:text-5xl">
            Scale intelligence without growing headcount
          </h2>
          <p className="mt-5 max-w-2xl text-lg text-muted">
            Give every analyst and executive a dedicated lens — SentinelX agents are always on. When human judgment is
            needed, you will know.
          </p>
        </FadeInUp>

        <StaggerReveal className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {benefits.map((benefit) => (
            <StaggerItem key={benefit.title}>
              <div className="h-full rounded-2xl border border-border bg-card-solid p-6 shadow-card transition hover:-translate-y-1 hover:shadow-soft">
                <h3 className="text-lg font-semibold text-foreground">{benefit.title}</h3>
                <p className="mt-3 text-sm leading-relaxed text-muted">{benefit.body}</p>
              </div>
            </StaggerItem>
          ))}
        </StaggerReveal>
      </div>
    </section>
  );
}
