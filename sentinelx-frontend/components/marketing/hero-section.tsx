'use client';

import { ArrowRight } from 'lucide-react';
import { DemoShowcase } from '@/components/marketing/demo-showcase';
import { FadeInUp, FloatSlow } from '@/components/marketing/motion';
import { CtaButton } from '@/components/ui/cta-button';
import { CHAMPENG } from '@/lib/champeng';

const stats = [
  { value: '6', label: 'specialized AI agents' },
  { value: '24/7', label: 'pipeline-ready monitoring' },
];

export function HeroSection() {
  return (
    <section className="relative overflow-hidden px-4 pb-16 pt-12 lg:px-8 lg:pb-24 lg:pt-16">
      <div className="mx-auto grid max-w-6xl gap-12 lg:grid-cols-[1fr_1.05fr] lg:items-center lg:gap-16">
        <FadeInUp>
          <h1 className="font-display text-[2.75rem] leading-[1.05] tracking-tight text-foreground sm:text-6xl lg:text-[4.25rem]">
            Intelligence for {CHAMPENG.companyName}
          </h1>
          <p className="mt-6 max-w-lg text-lg leading-relaxed text-muted sm:text-xl">
            {CHAMPENG.tagline}
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-4">
            <CtaButton href="/dashboard" variant="warm" size="lg">
              See live dashboard
              <ArrowRight className="h-4 w-4 shrink-0" aria-hidden />
            </CtaButton>
            <CtaButton href="#platform" variant="secondary" size="md">
              View platform
            </CtaButton>
          </div>

          <div className="mt-12 flex flex-wrap gap-10 border-t border-border pt-10">
            {stats.map((stat, index) => (
              <FadeInUp key={stat.label} delay={0.1 + index * 0.08}>
                <div>
                  <p className="font-display text-4xl tracking-tight text-foreground sm:text-5xl">{stat.value}</p>
                  <p className="mt-1 max-w-[12rem] text-sm leading-snug text-muted">{stat.label}</p>
                </div>
              </FadeInUp>
            ))}
          </div>
        </FadeInUp>

        <FloatSlow className="relative">
          <FadeInUp delay={0.15}>
            <DemoShowcase />
          </FadeInUp>
        </FloatSlow>
      </div>
    </section>
  );
}
