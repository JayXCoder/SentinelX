"use client";

import { useCallback, useEffect, useState } from 'react';
import { apiClient, getApiErrorMessage } from '@/lib/api-client';
import type { AlertsDto } from '@/lib/dto';

export function useAlerts() {
  const [data, setData] = useState<AlertsDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    setLoading(true);
    setError(null);

    return apiClient
      .getAlerts()
      .then((response) => setData(response))
      .catch((err: unknown) => setError(getApiErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return { data, loading, error, refresh };
}
