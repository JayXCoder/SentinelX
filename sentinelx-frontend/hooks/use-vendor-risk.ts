"use client";

import { useCallback, useEffect, useState } from 'react';
import { apiClient, getApiErrorMessage } from '@/lib/api-client';
import type { VendorRiskDto } from '@/lib/dto';

export function useVendorRisk() {
  const [data, setData] = useState<VendorRiskDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    setLoading(true);
    setError(null);

    return apiClient
      .getVendorSummary()
      .then((response) => setData(response))
      .catch((err: unknown) => setError(getApiErrorMessage(err)))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return { data, loading, error, refresh };
}
