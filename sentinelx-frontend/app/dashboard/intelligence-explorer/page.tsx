"use client";

import { dashboardCardClass, PageHeader } from '@/components/dashboard/page-header';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { useRagExplorer } from '@/hooks/use-rag-explorer';

export default function IntelligenceExplorerPage() {
  const { data, loading, error, ask } = useRagExplorer();

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Intelligence Explorer" title="Ask questions and explore evidence">
        RAG queries call the intelligence service when available. Until then, the UI shows a clear unavailable state.
      </PageHeader>

      <div className={dashboardCardClass}>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => void ask('What are the top SentinelX risks?')}
            className="btn-cta btn-cta--sm btn-cta--warm"
          >
            Ask sample question
          </button>
          <button type="button" className="btn-cta-secondary">
            Explore evidence
          </button>
        </div>

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
          </div>
        ) : (
          <p className="mt-4 rounded-2xl border border-border bg-background p-5 text-sm text-muted">
            Ask a question to query the RAG endpoint.
          </p>
        )}
      </div>
    </section>
  );
}
