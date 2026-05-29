"use client";

import { useState } from 'react';
import { apiClient, getApiErrorMessage } from '@/lib/api-client';
import type { RagAnswerDto } from '@/lib/dto';

export function useRagExplorer() {
  const [data, setData] = useState<RagAnswerDto | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const ask = async (question: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.askRagQuestion(question);
      setData(response);
      return response;
    } catch (err) {
      const message = getApiErrorMessage(err);
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, ask };
}
