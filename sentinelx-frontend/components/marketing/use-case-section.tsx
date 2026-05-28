'use client';

import { FadeInUp } from '@/components/marketing/motion';

const useCases = [
  {
    id: 'cyber',
    badge: 'Cyber intelligence',
    title: 'Help teams validate threats with AI context',
    gradient: 'from-[#ffd4c8] via-[#fce7f3] to-[#dcd2ff]',
    darkGradient: 'from-[#4a2820] via-[#3a2848] to-[#283050]',
    points: [
      {
        title: 'Engages analysts and answers in real time',
        body: 'Surfaces CVEs, breach mentions, and exposure signals as they appear across your monitored sources.',
      },
      {
        title: 'Qualifies severity and nudges response',
        body: 'Filters noise, highlights high-value incidents, and guides teams toward the right next action.',
      },
      {
        title: 'Retains memory and passes context',
        body: 'Remembers entities and timelines so every agent shares continuity across the dashboard.',
      },
    ],
  },
  {
    id: 'gtm',
    badge: 'GTM intelligence',
    title: 'Give 1:1 market insight at scale with an AI analyst',
    gradient: 'from-[#e8dff8] via-[#fce7f3] to-[#ffd4c8]',
    darkGradient: 'from-[#302848] via-[#3a2848] to-[#4a2820]',
    points: [
      {
        title: 'Runs deep-dive competitor sessions',
        body: 'Tracks pricing, launches, hiring, and sentiment with structured intelligence cards.',
      },
      {
        title: 'Gathers insights from every signal',
        body: 'Captures needs, entities, and confidence directly from agent-generated summaries.',
      },
      {
        title: 'Turns signals into opportunities',
        body: 'Equips revenue teams with evidence-backed context before prospects enter the CRM.',
      },
    ],
  },
  {
    id: 'vendor',
    badge: 'Vendor risk',
    title: 'Provide tailored vendor monitoring with an AI guide',
    gradient: 'from-[#d4e8ff] via-[#e8dff8] to-[#fce7f3]',
    darkGradient: 'from-[#203048] via-[#302848] to-[#3a2848]',
    points: [
      {
        title: 'Knows your vendor landscape',
        body: 'Ingests risk signals, outage mentions, and breach intelligence — kept current by the pipeline.',
      },
      {
        title: 'Scores posture in one view',
        body: 'Shows vendor health, severity trends, and recommended actions in a clean operations UI.',
      },
      {
        title: 'Helps teams reach decisions faster',
        body: 'Tailors monitoring per strategic supplier, boosting response time when incidents spike.',
      },
    ],
  },
];

export function UseCaseSection() {
  return (
    <section id="capabilities" className="border-t border-border px-4 py-20 lg:px-8 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <FadeInUp>
          <h2 className="font-display text-4xl tracking-tight text-foreground sm:text-5xl">
            Deploy agents across your intelligence journey
          </h2>
          <p className="mt-5 max-w-2xl text-lg leading-relaxed text-muted">
            Most security and revenue workflows are full of noise. Let SentinelX agents guide your teams from raw signal
            to executive-ready insight.
          </p>
        </FadeInUp>

        <div className="mt-16 space-y-24">
          {useCases.map((useCase, index) => (
            <FadeInUp key={useCase.id} delay={index * 0.05}>
              <article className="grid gap-10 lg:grid-cols-2 lg:items-center lg:gap-16">
                <div className={index % 2 === 1 ? 'lg:order-2' : ''}>
                  <p className="text-sm font-medium text-accent">{useCase.badge}</p>
                  <h3 className="mt-3 font-display text-3xl leading-tight tracking-tight text-foreground sm:text-4xl">
                    {useCase.title}
                  </h3>
                  <ul className="mt-8 space-y-6">
                    {useCase.points.map((point) => (
                      <li key={point.title}>
                        <p className="font-medium text-foreground">{point.title}</p>
                        <p className="mt-2 text-sm leading-relaxed text-muted">{point.body}</p>
                      </li>
                    ))}
                  </ul>
                </div>

                <div
                  className={`relative min-h-[240px] overflow-hidden rounded-3xl border border-border shadow-card sm:min-h-[280px] ${
                    index % 2 === 1 ? 'lg:order-1' : ''
                  }`}
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${useCase.gradient} dark:hidden`} aria-hidden />
                  <div
                    className={`absolute inset-0 hidden bg-gradient-to-br ${useCase.darkGradient} dark:block`}
                    aria-hidden
                  />
                  <div className="grain relative flex h-full min-h-[240px] flex-col justify-end p-6 sm:min-h-[280px] sm:p-8">
                    <div className="rounded-2xl border border-border/50 bg-card-solid/90 p-5 backdrop-blur">
                      <p className="text-xs font-medium uppercase tracking-widest text-muted">Agent preview</p>
                      <p className="mt-2 font-display text-xl text-foreground">{useCase.badge}</p>
                      <div className="mt-4 h-2 overflow-hidden rounded-full bg-border">
                        <div className="h-full w-3/4 rounded-full bg-accent transition-all duration-700" />
                      </div>
                    </div>
                  </div>
                </div>
              </article>
            </FadeInUp>
          ))}
        </div>
      </div>
    </section>
  );
}
