"use client";

import { useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { createWebSocketClient } from '@/lib/websocket-client';
import { useDashboardStore } from '@/stores/dashboard-store';
import type { CorrelatedEvent, IntelligenceSignal, RiskScore } from '@/types/sentinelx';

const notifyId = () => (globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`);
const POLL_INTERVAL_MS = 30_000;

export function useRealtimeEvents() {
  useEffect(() => {
    let pollTimer: ReturnType<typeof setInterval> | undefined;
    let lastSignalCount = 0;
    let connectTimeout: ReturnType<typeof setTimeout> | undefined;

    const stopPolling = () => {
      if (pollTimer) {
        clearInterval(pollTimer);
        pollTimer = undefined;
      }
    };

    const handlePayload = (event: { type: string; data: unknown }) => {
      const current = useDashboardStore.getState();

      if (event.type === 'new_signal') {
        current.addLiveSignal(event.data as IntelligenceSignal);
        current.pushNotification({
          id: notifyId(),
          title: 'New signal received',
          body: 'A live intelligence signal was added to the dashboard.',
          tone: 'info',
        });
      }

      if (event.type === 'new_correlated_event') {
        current.addLiveEvent(event.data as CorrelatedEvent);
        current.pushNotification({
          id: notifyId(),
          title: 'New correlated event',
          body: 'A new correlated event is now available for review.',
          tone: 'warning',
        });
      }

      if (event.type === 'new_risk_score') {
        current.addLiveRiskScore(event.data as RiskScore);
        current.pushNotification({
          id: notifyId(),
          title: 'Risk score updated',
          body: 'A new risk score was pushed from the intelligence service.',
          tone: 'success',
        });
      }

      if (event.type === 'new_alert') {
        const alert = event.data as { title?: string; explanation?: string };
        current.pushNotification({
          id: notifyId(),
          title: alert.title ?? 'New alert',
          body: alert.explanation ?? 'A new alert requires review.',
          tone: 'critical',
        });
      }

      if (event.type === 'system_status_update') {
        const status = (event.data as { status?: string })?.status;
        if (status === 'connected') return;
        current.pushNotification({
          id: notifyId(),
          title: 'System status update',
          body: 'SentinelX system status changed.',
          tone: 'info',
        });
      }
    };

    const startPolling = () => {
      if (pollTimer) return;
      useDashboardStore.getState().setRealtimeStatus('polling');
      pollTimer = setInterval(() => {
        void apiClient.getSignals(undefined, 5).then((signals) => {
          if (signals.length > lastSignalCount) {
            const newest = signals[0];
            if (newest) handlePayload({ type: 'new_signal', data: newest });
          }
          lastSignalCount = signals.length;
        });
      }, POLL_INTERVAL_MS);
    };

    let socket: WebSocket | undefined;
    let cancelled = false;

    void createWebSocketClient({
      onMessage: handlePayload,
      onOpen: () => {
        if (connectTimeout) clearTimeout(connectTimeout);
        stopPolling();
        useDashboardStore.getState().setRealtimeStatus('connected');
      },
      onClose: () => {
        useDashboardStore.getState().setRealtimeStatus('offline');
        startPolling();
      },
      onError: () => {
        socket?.close();
      },
    })
      .then((client) => {
        if (cancelled) {
          client.close();
          return;
        }
        socket = client;
        connectTimeout = setTimeout(() => {
          if (socket && socket.readyState !== WebSocket.OPEN) {
            socket.close();
            startPolling();
          }
        }, 2500);
      })
      .catch(() => {
        startPolling();
      });

    void apiClient.getSignals(undefined, 5).then((signals) => {
      lastSignalCount = signals.length;
    });

    return () => {
      cancelled = true;
      if (connectTimeout) clearTimeout(connectTimeout);
      stopPolling();
      socket?.close();
      useDashboardStore.getState().setRealtimeStatus('offline');
    };
  }, []);
}
