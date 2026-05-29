'use client';

import { ArrowRight } from 'lucide-react';
import { FadeInUp, StaggerItem, StaggerReveal } from '@/components/marketing/motion';
import { CtaButton } from '@/components/ui/cta-button';

const steps = [
  {
    step: '1',
    title: 'Link your sources & knowledge base',
    body: 'Connect scrape targets, feeds, and internal context into the SentinelX pipeline.',
  },
  {
    step: '2',
    title: 'Agents generate intelligence — you refine',
    body: 'Cyber, GTM, vendor, and executive agents produce signals you tune for your organization.',
  },
  {
    step: '3',
    title: 'Deploy the dashboard for your team',
    body: 'Open the command center with live feeds, alerts, and exploration — no heavy integration required.',
  },
];

export function StepsSection() {
  return (
    <section id="how-it-works" className="border-t border-border bg-elevated/50 px-4 py-20 lg:px-8 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <FadeInUp>
          <h2 className="font-display text-4xl tracking-tight text-foreground sm:text-5xl">Get started in minutes</h2>
        </FadeInUp>

        <div className="mt-14 grid gap-12 lg:grid-cols-[1fr_1.1fr] lg:items-center">
          <StaggerReveal className="space-y-10">
            {steps.map((item) => (
              <StaggerItem key={item.step}>
                <li className="flex list-none gap-6">
                  <span className="font-display text-5xl leading-none text-muted/40">{item.step}</span>
                  <div>
                    <h3 className="text-lg font-medium text-foreground">{item.title}</h3>
                    <p className="mt-2 text-sm leading-relaxed text-muted">{item.body}</p>
                  </div>
                </li>
              </StaggerItem>
            ))}
          </StaggerReveal>

          <FadeInUp delay={0.12}>
            <div className="relative overflow-hidden rounded-3xl border border-border bg-[var(--sx-gradient-hero)] p-8 shadow-soft">
              <div className="space-y-4 rounded-2xl border border-border/60 bg-card-solid/95 p-6 backdrop-blur">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted">Pipeline status</span>
                  <span className="rounded-full bg-emerald-500/15 px-2.5 py-0.5 text-xs font-medium text-emerald-700 dark:text-emerald-300">
                    Healthy
                  </span>
                </div>
                <div className="space-y-2">
                  {['Scrape', 'Parse', 'Agents', 'Dashboard'].map((stage, i) => (
                    <div key={stage} className="flex items-center gap-3">
                      <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent-soft text-xs font-medium text-accent">
                        {i + 1}
                      </span>
                      <span className="text-sm text-foreground">{stage}</span>
                    </div>
                  ))}
                </div>
              </div>
              <p className="mt-6 text-center text-sm text-muted">First signals in minutes · production-ready in days</p>
            </div>
          </FadeInUp>
        </div>

        <FadeInUp className="mt-12" delay={0.1}>
          <CtaButton href="/dashboard" variant="solid" size="md">
            Get started
            <ArrowRight className="h-4 w-4 shrink-0" aria-hidden />
          </CtaButton>
        </FadeInUp>
      </div>
    </section>
  );
}
