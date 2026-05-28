import { create } from 'zustand';

export type Theme = 'light' | 'dark';

type ThemeState = {
  theme: Theme;
  mounted: boolean;
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
  setMounted: (mounted: boolean) => void;
};

export const useThemeStore = create<ThemeState>((set, get) => ({
  theme: 'light',
  mounted: false,
  setTheme: (theme) => set({ theme }),
  toggleTheme: () => set({ theme: get().theme === 'light' ? 'dark' : 'light' }),
  setMounted: (mounted) => set({ mounted }),
}));
