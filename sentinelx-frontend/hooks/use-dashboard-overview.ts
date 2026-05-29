"use client";

import { useEffect, useState } from 'react';
import { apiClient, getApiErrorMessage } from '@/lib/api-client';
import type { DashboardOverviewDto } from '@/lib/dto';

export function useDashboardOverview() {
  const [data, setData] = useState<DashboardOverviewDto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    apiClient
      .getDashboardOverview()
      .then((response) => {
        if (!active) return;
        setData(response);
      })
      .catch((err: unknown) => {
        if (!active) return;
        setError(getApiErrorMessage(err));
      })
      .finally(() => {
        if (!active) return;
        setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  return { data, loading, error };
}
