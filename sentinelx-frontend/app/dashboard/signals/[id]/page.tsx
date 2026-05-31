'use client';

import { useParams, useSearchParams } from 'next/navigation';
import { Suspense, useEffect, useState } from 'react';
import { IntelligenceDetailView } from '@/components/dashboard/intelligence-detail-view';
import { ErrorState } from '@/components/dashboard/error-state';
import { LoadingState } from '@/components/dashboard/loading-state';
import { apiClient, getApiErrorMessage } from '@/lib/api-client';
import type { SignalDetail } from '@/types/signal-detail';

function SignalDetailContent() {
  const params = useParams();
  const searchParams = useSearchParams();
  const signalId = String(params.id);
  const backHref = searchParams.get('from') ?? '/dashboard/threat-feed';
  const backLabel = searchParams.get('fromLabel') ?? 'Back to feed';

  const [detail, setDetail] = useState<SignalDetail | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    void apiClient
      .getSignalDetail(signalId)
      .then(setDetail)
      .catch((e) => setError(getApiErrorMessage(e)))
      .finally(() => setLoading(false));
  }, [signalId]);

  if (loading) return <LoadingState label="Loading intelligence detail…" />;
  if (error) return <ErrorState message={error} />;
  if (!detail) return <ErrorState message="Signal not found" />;

  return (
    <IntelligenceDetailView detail={detail} backHref={backHref} backLabel={backLabel} />
  );
}

export default function SignalDetailPage() {
  return (
    <Suspense fallback={<LoadingState label="Loading intelligence detail…" />}>
      <SignalDetailContent />
    </Suspense>
  );
}
