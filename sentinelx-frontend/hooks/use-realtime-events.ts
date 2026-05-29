"use client";

import { useEffect } from 'react';
import { createWebSocketClient } from '@/lib/websocket-client';
import { useDashboardStore } from '@/stores/dashboard-store';
import type { CorrelatedEvent, IntelligenceSignal, RiskScore } from '@/types/sentinelx';

const notifyId = () => (globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`);

export function useRealtimeEvents() {
  useEffect(() => {
    const socket = createWebSocketClient((event) => {
      const store = useDashboardStore.getState();

      if (event.type === 'new_signal') {
        store.addLiveSignal(event.data as IntelligenceSignal);
        store.pushNotification({ id: notifyId(), title: 'New signal received', body: 'A live intelligence signal was added to the dashboard.', tone: 'info' });
      }

      if (event.type === 'new_correlated_event') {
        store.addLiveEvent(event.data as CorrelatedEvent);
        store.pushNotification({ id: notifyId(), title: 'New correlated event', body: 'A new correlated event is now available for review.', tone: 'warning' });
      }

      if (event.type === 'new_risk_score') {
        store.addLiveRiskScore(event.data as RiskScore);
        store.pushNotification({ id: notifyId(), title: 'Risk score updated', body: 'A new risk score was pushed from the backend.', tone: 'success' });
      }

      if (event.type === 'new_alert') {
        store.pushNotification({ id: notifyId(), title: 'New alert', body: 'A new alert requires review.', tone: 'critical' });
      }

      if (event.type === 'system_status_update') {
        store.pushNotification({ id: notifyId(), title: 'System status update', body: 'SentinelX system status changed.', tone: 'info' });
      }
    });

    return () => {
      socket.close();
    };
  }, []);
}
