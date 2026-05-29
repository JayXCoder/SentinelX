'use client';

import { Bot, Database, Layers, Radar, Shield, Sparkles } from 'lucide-react';
import { FadeInUp, StaggerItem, StaggerReveal } from '@/components/marketing/motion';

const capabilities = [
  {
    icon: Radar,
    title: 'Live web ingestion',
    body: 'Scrape and monitor sources via Bright Data (or HTTP fallback), with retries, job orchestration, and raw record storage.',
  },
  {
    icon: Layers,
    title: 'Parse → agent pipeline',
    body: 'HTML parsing and cleaning feed six Qwen-powered agents: cyber, GTM, financial, vendor risk, OSINT, and executive summary.',
  },
  {
    icon: Database,
    title: 'Durable intelligence store',
    body: 'Signals land in PostgreSQL with vector embeddings in Qdrant — ready for search, dashboards, and downstream correlation.',
  },
  {
    icon: Shield,
    title: 'Operational dashboard',
    body: 'Threat feed, competitor/GTM signals, vendor risk, alerts, and an explorer UI wired to `GET /agents/signals` today.',
  },
  {
    icon: Bot,
    title: 'Redis stream workers',
    body: 'Celery workers consume scrape → parse → agent stages over Redis streams with monitoring endpoints for pipeline health.',
  },
  {
    icon: Sparkles,
    title: 'Roadmap: correlate & RAG',
    body: 'sentinelx-intelligence will add correlation, risk scoring, knowledge graph, and RAG answers — the frontend is already structured for it.',
  },
];

export function PlatformSection() {
  return (
    <section id="platform" className="border-t border-border bg-elevated/40 px-4 py-20 lg:px-8 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <FadeInUp>
          <p className="text-sm font-medium text-accent">What SentinelX ships today</p>
          <h2 className="mt-3 font-display text-4xl tracking-tight text-foreground sm:text-5xl">
            Built as an AI-native intelligence pipeline — not a slide deck
          </h2>
          <p className="mt-5 max-w-2xl text-lg leading-relaxed text-muted">
            Jay&apos;s backend handles ingestion and agents; Kai Zhe&apos;s intelligence layer adds correlation and RAG next.
            This dashboard is the product surface for everything in between.
          </p>
        </FadeInUp>

        <StaggerReveal className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {capabilities.map((item) => {
            const Icon = item.icon;
            return (
              <StaggerItem key={item.title}>
                <article className="flex h-full flex-col rounded-2xl border border-border bg-card-solid p-6 shadow-card transition hover:-translate-y-0.5 hover:shadow-soft">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-accent-soft text-accent">
                    <Icon className="h-5 w-5" aria-hidden />
                  </div>
                  <h3 className="mt-4 text-lg font-semibold text-foreground">{item.title}</h3>
                  <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">{item.body}</p>
                </article>
              </StaggerItem>
            );
          })}
        </StaggerReveal>
      </div>
    </section>
  );
}
