'use client';

import { FadeInUp } from '@/components/marketing/motion';

const faqs = [
  {
    q: 'How long does it take to set up?',
    a: 'You can connect sources and see the first pipeline run in minutes. Most teams refine agent output and go live with the dashboard within a few working days.',
  },
  {
    q: 'How do agents stay up to date?',
    a: 'SentinelX regularly syncs with your configured sources and knowledge base. Unanswered questions can be traced back to gaps in source coverage for quick fixes.',
  },
  {
    q: 'How is intelligence personalized?',
    a: 'Agents tailor summaries and severity to the entities and signal types you monitor. Executive summaries aggregate the highest-impact items for leadership.',
  },
  {
    q: 'What domains does SentinelX cover?',
    a: 'Cyber, GTM, financial, vendor risk, OSINT, and executive summary agents — with correlation and RAG expanding as the intelligence service comes online.',
  },
  {
    q: 'What analytics are available?',
    a: 'The dashboard shows live signals, alerts, vendor posture, and exploration views. Full transcripts and export will deepen as the platform matures.',
  },
  {
    q: 'Can I connect my existing backend?',
    a: 'Yes. The frontend reads from the FastAPI backend today (/agents/signals) and will integrate correlation, scoring, and RAG endpoints as they ship.',
  },
];

export function FaqSection() {
  return (
    <section id="faq" className="border-t border-border px-4 py-20 lg:px-8 lg:py-28">
      <div className="mx-auto max-w-3xl">
        <FadeInUp>
          <h2 className="font-display text-4xl tracking-tight text-foreground">Frequently asked questions</h2>
        </FadeInUp>

        <div className="mt-10 divide-y divide-border rounded-2xl border border-border bg-card-solid">
          {faqs.map((faq, index) => (
            <FadeInUp key={faq.q} delay={index * 0.04}>
              <details className="group px-6 py-5">
                <summary className="cursor-pointer list-none text-base font-medium text-foreground marker:content-none [&::-webkit-details-marker]:hidden">
                  <span className="flex items-center justify-between gap-4">
                    {faq.q}
                    <span className="text-xl text-muted transition group-open:rotate-45" aria-hidden>
                      +
                    </span>
                  </span>
                </summary>
                <p className="mt-4 text-sm leading-relaxed text-muted">{faq.a}</p>
              </details>
            </FadeInUp>
          ))}
        </div>
      </div>
    </section>
  );
}
