import { create } from 'zustand';
import type { CorrelatedEvent, IntelligenceSignal, RiskScore } from '@/types/sentinelx';

export type TimeRange = '24h' | '7d' | '30d';

export type NotificationItem = {
  id: string;
  title: string;
  body: string;
  tone: 'info' | 'success' | 'warning' | 'critical';
};

export type DashboardState = {
  selectedEntity: string | null;
  selectedRiskLevel: 'all' | 'low' | 'medium' | 'high' | 'critical';
  selectedTimeRange: TimeRange;
  sidebarOpen: boolean;
  liveSignals: IntelligenceSignal[];
  liveEvents: CorrelatedEvent[];
  liveRiskScores: RiskScore[];
  notifications: NotificationItem[];
  setSelectedEntity: (entity: string | null) => void;
  setSelectedRiskLevel: (level: DashboardState['selectedRiskLevel']) => void;
  setSelectedTimeRange: (range: TimeRange) => void;
  setSidebarOpen: (open: boolean) => void;
  pushNotification: (notification: NotificationItem) => void;
  addLiveSignal: (signal: IntelligenceSignal) => void;
  addLiveEvent: (event: CorrelatedEvent) => void;
  addLiveRiskScore: (score: RiskScore) => void;
  clearNotifications: () => void;
};

export const useDashboardStore = create<DashboardState>((set) => ({
  selectedEntity: null,
  selectedRiskLevel: 'all',
  selectedTimeRange: '7d',
  sidebarOpen: false,
  liveSignals: [],
  liveEvents: [],
  liveRiskScores: [],
  notifications: [],
  setSelectedEntity: (selectedEntity) => set({ selectedEntity }),
  setSelectedRiskLevel: (selectedRiskLevel) => set({ selectedRiskLevel }),
  setSelectedTimeRange: (selectedTimeRange) => set({ selectedTimeRange }),
  setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
  pushNotification: (notification) => set((state) => ({ notifications: [notification, ...state.notifications].slice(0, 5) })),
  addLiveSignal: (signal) => set((state) => ({ liveSignals: [signal, ...state.liveSignals].slice(0, 10) })),
  addLiveEvent: (event) => set((state) => ({ liveEvents: [event, ...state.liveEvents].slice(0, 10) })),
  addLiveRiskScore: (score) => set((state) => ({ liveRiskScores: [score, ...state.liveRiskScores].slice(0, 10) })),
  clearNotifications: () => set({ notifications: [] }),
}));
