"use client";

import { useCallback, useEffect, useState } from 'react';
import { apiClient, getApiErrorMessage } from '@/lib/api-client';
import type { CompetitorIntelligenceDto } from '@/lib/dto';

export function useCompetitorIntelligence() {
  const [data, setData] = useState<CompetitorIntelligenceDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    setLoading(true);
    setError(null);

    return apiClient
      .getGtmSignals()
      .then((response) => setData(response))
      .catch((err: unknown) => setError(getApiErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return { data, loading, error, refresh };
}
