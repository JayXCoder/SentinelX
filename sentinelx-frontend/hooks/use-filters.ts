import { useDashboardStore } from '@/stores/dashboard-store';

export function useFilters() {
  const selectedEntity = useDashboardStore((state) => state.selectedEntity);
  const selectedRiskLevel = useDashboardStore((state) => state.selectedRiskLevel);
  const selectedTimeRange = useDashboardStore((state) => state.selectedTimeRange);
  const setSelectedEntity = useDashboardStore((state) => state.setSelectedEntity);
  const setSelectedRiskLevel = useDashboardStore((state) => state.setSelectedRiskLevel);
  const setSelectedTimeRange = useDashboardStore((state) => state.setSelectedTimeRange);

  return {
    selectedEntity,
    selectedRiskLevel,
    selectedTimeRange,
    setSelectedEntity,
    setSelectedRiskLevel,
    setSelectedTimeRange,
  };
}
