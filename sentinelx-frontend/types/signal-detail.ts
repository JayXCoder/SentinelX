import type { IntelligenceSignal } from '@/types/sentinelx';

export type SourceProvenance = {
  source_id: string;
  source_name: string;
  source_url: string;
  source_type: string;
  category?: string | null;
};

export type RecordExcerpt = {
  parsed_record_id: string;
  title?: string | null;
  excerpt: string;
  url?: string | null;
  fetched_at?: string | null;
  content_hash?: string | null;
};

export type StoryEvent = {
  id: string;
  event_type: string;
  title: string;
  summary: string;
  occurred_at: string;
  severity: number;
  source_label?: string | null;
};

export type HumanNote = {
  id: string;
  team_role: string;
  author_name: string;
  content: string;
  created_at: string;
};

export type SignalDetail = {
  signal: IntelligenceSignal;
  source: SourceProvenance;
  record: RecordExcerpt;
  related_signals: IntelligenceSignal[];
  story_timeline: StoryEvent[];
  human_notes: HumanNote[];
};

export type WorkspaceProfile = {
  id: string;
  slug: string;
  company_name: string;
  profile: Record<string, unknown>;
  updated_at: string;
};
