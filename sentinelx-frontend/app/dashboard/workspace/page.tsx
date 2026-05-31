'use client';

import { useCallback, useEffect, useState } from 'react';
import { PageHeader, dashboardButtonClass, dashboardCardClass } from '@/components/dashboard/page-header';
import { LoadingState } from '@/components/dashboard/loading-state';
import { ErrorState } from '@/components/dashboard/error-state';
import { apiClient, getApiErrorMessage } from '@/lib/api-client';
import type { WorkspaceProfile } from '@/types/signal-detail';

type SourceRow = {
  id: string;
  name: string;
  base_url: string;
  category?: string | null;
  is_active: boolean;
};

export default function WorkspacePage() {
  const [profile, setProfile] = useState<WorkspaceProfile | null>(null);
  const [sources, setSources] = useState<SourceRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [productSummary, setProductSummary] = useState('');
  const [newCompetitorName, setNewCompetitorName] = useState('');
  const [newCompetitorUrl, setNewCompetitorUrl] = useState('');
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [p, s] = await Promise.all([
        apiClient.getWorkspaceProfile(),
        apiClient.listSources(),
      ]);
      setProfile(p);
      setProductSummary(String((p.profile as { product_summary?: string }).product_summary ?? ''));
      setSources(s);
      setError(null);
    } catch (e) {
      setError(getApiErrorMessage(e));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const saveProfile = async () => {
    setSaving(true);
    try {
      const updated = await apiClient.updateWorkspaceProfile({
        profile: { product_summary: productSummary },
      });
      setProfile(updated);
    } catch (e) {
      setError(getApiErrorMessage(e));
    } finally {
      setSaving(false);
    }
  };

  const addCompetitorSource = async () => {
    if (!newCompetitorName.trim() || !newCompetitorUrl.trim()) return;
    const slug = newCompetitorName.toLowerCase().replace(/\s+/g, '_');
    await apiClient.createSource({
      name: `${newCompetitorName} News`,
      source_type: 'web',
      base_url: newCompetitorUrl,
      category: `competitor_${slug}`,
      scraping_strategy: 'browser',
    });
    setNewCompetitorName('');
    setNewCompetitorUrl('');
    await load();
  };

  if (loading) return <LoadingState label="Loading workspace…" />;
  if (error && !profile) return <ErrorState message={error} />;

  return (
    <section className="space-y-6">
      <PageHeader eyebrow="Human in the loop" title="ChamPeng workspace">
        HR, sales, and engineering teams can enrich company context, add competitor sources, and steer
        SentinelX without re-burning scrape credits on unchanged pages.
      </PageHeader>

      <div className="grid gap-4 sm:grid-cols-3">
        {(['hr', 'sales', 'tech'] as const).map((team) => (
          <div key={team} className={dashboardCardClass}>
            <h3 className="text-sm font-semibold uppercase tracking-wide text-accent">{team}</h3>
            <p className="mt-2 text-sm text-muted">
              {(profile?.profile as { team_lenses?: Record<string, string> })?.team_lenses?.[team] ??
                `Use ${team} lens on any signal detail page to add notes and ask AI.`}
            </p>
          </div>
        ))}
      </div>

      <div className={dashboardCardClass}>
        <h2 className="text-lg font-medium text-foreground">Company context for AI</h2>
        <p className="mt-1 text-sm text-muted">
          This text is injected into every RAG answer so comparisons vs OpenAI, Cursor, and others stay
          ChamPeng-specific.
        </p>
        <textarea
          value={productSummary}
          onChange={(e) => setProductSummary(e.target.value)}
          rows={6}
          className="mt-4 w-full rounded-2xl border border-border bg-background px-4 py-3 text-sm"
        />
        <button
          type="button"
          disabled={saving}
          onClick={() => void saveProfile()}
          className="btn-cta btn-cta--warm mt-3"
        >
          {saving ? 'Saving…' : 'Save context'}
        </button>
      </div>

      <div className={dashboardCardClass}>
        <h2 className="text-lg font-medium text-foreground">Monitored sources</h2>
        <p className="mt-1 text-sm text-muted">
          Historical snapshots are kept in Postgres. Re-scrapes within 24h reuse cached HTML (no Bright Data
          charge).
        </p>
        <ul className="mt-4 divide-y divide-border">
          {sources.map((s) => (
            <li key={s.id} className="flex flex-wrap items-center justify-between gap-2 py-3">
              <div>
                <p className="font-medium text-foreground">{s.name}</p>
                <p className="text-xs text-muted">{s.category ?? 'uncategorized'}</p>
                <a href={s.base_url} className="text-xs text-accent hover:underline" target="_blank" rel="noreferrer">
                  {s.base_url}
                </a>
              </div>
              <span
                className={`rounded-full px-2 py-0.5 text-xs ${s.is_active ? 'bg-green-500/10 text-green-700' : 'bg-muted text-muted-foreground'}`}
              >
                {s.is_active ? 'active' : 'paused'}
              </span>
            </li>
          ))}
        </ul>

        <h3 className="mt-6 text-sm font-semibold text-foreground">Add competitor source</h3>
        <div className="mt-3 grid gap-3 sm:grid-cols-2">
          <input
            placeholder="Competitor name"
            value={newCompetitorName}
            onChange={(e) => setNewCompetitorName(e.target.value)}
            className="rounded-xl border border-border bg-background px-3 py-2 text-sm"
          />
          <input
            placeholder="https://competitor.com/news"
            value={newCompetitorUrl}
            onChange={(e) => setNewCompetitorUrl(e.target.value)}
            className="rounded-xl border border-border bg-background px-3 py-2 text-sm"
          />
        </div>
        <button type="button" onClick={() => void addCompetitorSource()} className={dashboardButtonClass}>
          Add source
        </button>
      </div>
    </section>
  );
}
