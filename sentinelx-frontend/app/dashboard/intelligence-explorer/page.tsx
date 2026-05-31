"use client";

import { useState } from 'react';
import { dashboardCardClass, PageHeader } from '@/components/dashboard/page-header';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { Input } from '@/components/ui/input';
import { useRagExplorer } from '@/hooks/use-rag-explorer';
import { CHAMPENG } from '@/lib/champeng';

export default function IntelligenceExplorerPage() {
  const { data, loading, error, ask } = useRagExplorer();
  const [question, setQuestion] = useState(CHAMPENG.defaultRagQuestion);

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Intelligence Explorer" title="Ask questions and explore evidence">
        Natural-language queries are answered by the intelligence RAG service with supporting evidence and related
        entities.
      </PageHeader>

      <div className={dashboardCardClass}>
        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault();
            void ask(question);
          }}
        >
          <Input
            label="Your question"
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask about risks, vendors, competitors, or incidents"
          />
          <div className="flex flex-wrap gap-3">
            <button type="submit" disabled={loading} className="btn-cta btn-cta--sm btn-cta--warm">
              {loading ? 'Generating…' : 'Ask SentinelX'}
            </button>
            <button
              type="button"
              onClick={() => setQuestion('Summarize critical vendor and cyber risks.')}
              className="btn-cta-secondary"
            >
              Sample: vendor + cyber summary
            </button>
          </div>
        </form>

        {loading ? (
          <div className="mt-4">
            <LoadingState label="Generating answer..." />
          </div>
        ) : error ? (
          <div className="mt-4">
            <ErrorState message={error} />
          </div>
        ) : data ? (
          <div className="mt-4 space-y-4 rounded-2xl border border-border bg-background p-5">
            <p className="text-sm leading-7 text-foreground">{data.answer}</p>
            <p className="text-xs text-muted">Confidence: {(data.confidence * 100).toFixed(0)}%</p>
            {data.recommended_action ? (
              <p className="text-sm text-foreground">
                <span className="font-medium">Recommended action:</span> {data.recommended_action}
              </p>
            ) : null}
            {data.supporting_evidence.length > 0 ? (
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-muted">Supporting evidence</p>
                <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted">
                  {data.supporting_evidence.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null}
            {data.related_entities.length > 0 ? (
              <p className="text-sm text-muted">
                Related entities: {data.related_entities.join(', ')}
              </p>
            ) : null}
          </div>
        ) : (
          <p className="mt-4 rounded-2xl border border-border bg-background p-5 text-sm text-muted">
            Ask a question to query the intelligence RAG endpoint.
          </p>
        )}
      </div>
    </section>
  );
}
