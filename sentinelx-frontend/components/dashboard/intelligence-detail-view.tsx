'use client';

import Link from 'next/link';
import { useCallback, useState } from 'react';
import { ExternalLink, MessageSquarePlus, Sparkles } from 'lucide-react';
import {
  dashboardButtonClass,
  dashboardCardClass,
} from '@/components/dashboard/page-header';
import { apiClient } from '@/lib/api-client';
import type { SignalDetail } from '@/types/signal-detail';
import type { RagAnswerDto } from '@/lib/dto';

const TEAM_ROLES = [
  { id: 'general', label: 'General' },
  { id: 'hr', label: 'HR' },
  { id: 'sales', label: 'Sales' },
  { id: 'tech', label: 'Tech' },
] as const;

type IntelligenceDetailViewProps = {
  detail: SignalDetail;
  backHref: string;
  backLabel: string;
};

export function IntelligenceDetailView({
  detail,
  backHref,
  backLabel,
}: IntelligenceDetailViewProps) {
  const { signal, source, record, related_signals, story_timeline, human_notes } =
    detail;
  const [question, setQuestion] = useState(
    `Explain this ${signal.signal_type} signal for ChamPeng and what HR, sales, and tech should do.`,
  );
  const [ragAnswer, setRagAnswer] = useState<RagAnswerDto | null>(null);
  const [ragLoading, setRagLoading] = useState(false);
  const [noteContent, setNoteContent] = useState('');
  const [noteRole, setNoteRole] = useState('general');
  const [noteAuthor, setNoteAuthor] = useState('');
  const [notes, setNotes] = useState(human_notes);

  const askAi = useCallback(async () => {
    setRagLoading(true);
    try {
      const answer = await apiClient.askRagWithContext({
        question,
        signalContext: [
          `Title: ${signal.title}`,
          `Type: ${signal.signal_type} / ${signal.category}`,
          `Summary: ${signal.summary}`,
          `Severity: ${signal.severity}`,
          `Entities: ${signal.entities.join(', ')}`,
          `Evidence: ${signal.evidence.join(' | ')}`,
          `Source: ${source.source_name} (${source.source_url})`,
          `Excerpt: ${record.excerpt.slice(0, 1500)}`,
        ].join('\n'),
      });
      setRagAnswer(answer);
    } finally {
      setRagLoading(false);
    }
  }, [question, signal, source, record]);

  const addNote = useCallback(async () => {
    if (!noteContent.trim()) return;
    const created = await apiClient.createNote({
      target_type: 'signal',
      target_id: signal.id,
      team_role: noteRole,
      author_name: noteAuthor.trim() || 'Analyst',
      content: noteContent.trim(),
    });
    setNotes((prev) => [created, ...prev]);
    setNoteContent('');
  }, [noteContent, noteRole, noteAuthor, signal.id]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-3">
        <Link href={backHref} className={dashboardButtonClass}>
          ← {backLabel}
        </Link>
        <span className="rounded-full border border-border bg-accent-soft px-3 py-1 text-xs font-semibold text-accent">
          {signal.signal_type}
        </span>
        <span className="text-xs text-muted">
          Severity {signal.severity} · {(signal.confidence * 100).toFixed(0)}% confidence
        </span>
      </div>

      <header className="space-y-2">
        <h1 className="text-2xl font-semibold text-foreground">{signal.title}</h1>
        <p className="text-sm text-muted">{signal.category}</p>
        <p className="text-base leading-relaxed text-foreground">{signal.summary}</p>
      </header>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className={dashboardCardClass}>
          <h2 className="text-lg font-medium text-foreground">Source & provenance</h2>
          <dl className="mt-4 space-y-2 text-sm">
            <div>
              <dt className="text-muted">Source</dt>
              <dd className="font-medium text-foreground">{source.source_name}</dd>
            </div>
            <div>
              <dt className="text-muted">URL</dt>
              <dd>
                <a
                  href={source.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 text-accent hover:underline"
                >
                  {source.source_url}
                  <ExternalLink className="h-3.5 w-3.5" aria-hidden />
                </a>
              </dd>
            </div>
            {source.category ? (
              <div>
                <dt className="text-muted">Category</dt>
                <dd className="text-foreground">{source.category}</dd>
              </div>
            ) : null}
            {record.fetched_at ? (
              <div>
                <dt className="text-muted">Fetched</dt>
                <dd className="text-foreground">
                  {new Date(record.fetched_at).toLocaleString()}
                </dd>
              </div>
            ) : null}
            <div>
              <dt className="text-muted">Source reliability</dt>
              <dd className="text-foreground">
                {(signal.source_reliability * 100).toFixed(0)}%
              </dd>
            </div>
          </dl>
        </section>

        <section className={dashboardCardClass}>
          <h2 className="text-lg font-medium text-foreground">Continuous story</h2>
          <ol className="mt-4 space-y-4 border-l border-border pl-4">
            {story_timeline.map((event) => (
              <li key={event.id} className="relative">
                <span className="absolute -left-[21px] top-1.5 h-2.5 w-2.5 rounded-full bg-accent" />
                <p className="text-xs text-muted">
                  {new Date(event.occurred_at).toLocaleString()}
                  {event.source_label ? ` · ${event.source_label}` : ''}
                </p>
                <p className="font-medium text-foreground">{event.title}</p>
                <p className="text-sm text-muted">{event.summary}</p>
              </li>
            ))}
          </ol>
        </section>
      </div>

      {signal.evidence.length > 0 ? (
        <section className={dashboardCardClass}>
          <h2 className="text-lg font-medium text-foreground">Evidence</h2>
          <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-foreground">
            {signal.evidence.map((item, i) => (
              <li key={`${i}-${item.slice(0, 24)}`}>{item}</li>
            ))}
          </ul>
        </section>
      ) : null}

      {signal.entities.length > 0 ? (
        <section className={dashboardCardClass}>
          <h2 className="text-lg font-medium text-foreground">Entities</h2>
          <div className="mt-3 flex flex-wrap gap-2">
            {signal.entities.map((entity) => (
              <span
                key={entity}
                className="rounded-full border border-border bg-card-solid px-3 py-1 text-xs text-foreground"
              >
                {entity}
              </span>
            ))}
          </div>
        </section>
      ) : null}

      {record.excerpt ? (
        <section className={dashboardCardClass}>
          <h2 className="text-lg font-medium text-foreground">Archived source excerpt</h2>
          <p className="mt-2 text-xs text-muted">
            Stored locally — re-scrapes within 24h reuse this snapshot (saves Bright Data credits).
          </p>
          <pre className="mt-3 max-h-64 overflow-auto whitespace-pre-wrap rounded-2xl border border-border bg-background p-4 text-xs text-muted">
            {record.excerpt}
          </pre>
        </section>
      ) : null}

      {signal.recommended_action ? (
        <section className={dashboardCardClass}>
          <h2 className="text-lg font-medium text-foreground">Recommended action</h2>
          <p className="mt-2 text-sm text-foreground">{signal.recommended_action}</p>
        </section>
      ) : null}

      {related_signals.length > 0 ? (
        <section className={dashboardCardClass}>
          <h2 className="text-lg font-medium text-foreground">Related intelligence</h2>
          <ul className="mt-4 divide-y divide-border">
            {related_signals.map((rel) => (
              <li key={rel.id} className="py-3 first:pt-0">
                <Link
                  href={`/dashboard/signals/${rel.id}`}
                  className="font-medium text-accent hover:underline"
                >
                  {rel.title}
                </Link>
                <p className="text-sm text-muted line-clamp-2">{rel.summary}</p>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <section className={dashboardCardClass}>
        <h2 className="flex items-center gap-2 text-lg font-medium text-foreground">
          <Sparkles className="h-5 w-5 text-accent" aria-hidden />
          Ask SentinelX (ChamPeng context)
        </h2>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows={3}
          className="mt-3 w-full rounded-2xl border border-border bg-background px-4 py-3 text-sm text-foreground"
        />
        <button
          type="button"
          disabled={ragLoading}
          onClick={() => void askAi()}
          className="btn-cta btn-cta--warm mt-3"
        >
          {ragLoading ? 'Analyzing…' : 'Ask AI'}
        </button>
        {ragAnswer ? (
          <div className="mt-4 space-y-3 rounded-2xl border border-border bg-accent-soft/30 p-4 text-sm">
            <p className="text-foreground">{ragAnswer.answer}</p>
            <p className="text-muted">
              Confidence: {(ragAnswer.confidence * 100).toFixed(0)}%
            </p>
            {ragAnswer.recommended_action ? (
              <p className="text-foreground">{ragAnswer.recommended_action}</p>
            ) : null}
            {ragAnswer.supporting_evidence?.length ? (
              <ul className="list-disc pl-5 text-muted">
                {ragAnswer.supporting_evidence.map((e, i) => (
                  <li key={i}>{e}</li>
                ))}
              </ul>
            ) : null}
          </div>
        ) : null}
      </section>

      <section className={dashboardCardClass}>
        <h2 className="flex items-center gap-2 text-lg font-medium text-foreground">
          <MessageSquarePlus className="h-5 w-5 text-accent" aria-hidden />
          Team notes (human in the loop)
        </h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <select
            value={noteRole}
            onChange={(e) => setNoteRole(e.target.value)}
            className="rounded-xl border border-border bg-background px-3 py-2 text-sm"
          >
            {TEAM_ROLES.map((r) => (
              <option key={r.id} value={r.id}>
                {r.label}
              </option>
            ))}
          </select>
          <input
            placeholder="Your name"
            value={noteAuthor}
            onChange={(e) => setNoteAuthor(e.target.value)}
            className="rounded-xl border border-border bg-background px-3 py-2 text-sm"
          />
        </div>
        <textarea
          value={noteContent}
          onChange={(e) => setNoteContent(e.target.value)}
          placeholder="Add interpretation for HR, sales, or engineering…"
          rows={3}
          className="mt-3 w-full rounded-2xl border border-border bg-background px-4 py-3 text-sm"
        />
        <button type="button" onClick={() => void addNote()} className={dashboardButtonClass}>
          Save note
        </button>
        <ul className="mt-4 space-y-3">
          {notes.map((note) => (
            <li
              key={note.id}
              className="rounded-2xl border border-border bg-card-solid p-4 text-sm"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-accent">
                {note.team_role} · {note.author_name}
              </p>
              <p className="mt-2 text-foreground">{note.content}</p>
              <p className="mt-1 text-xs text-muted">
                {new Date(note.created_at).toLocaleString()}
              </p>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
