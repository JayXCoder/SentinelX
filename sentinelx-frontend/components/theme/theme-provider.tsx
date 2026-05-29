'use client';

import { useEffect } from 'react';
import { useThemeStore } from '@/stores/theme-store';

export function ThemeProvider({ children }: Readonly<{ children: React.ReactNode }>) {
  const theme = useThemeStore((state) => state.theme);
  const setTheme = useThemeStore((state) => state.setTheme);
  const setMounted = useThemeStore((state) => state.setMounted);

  useEffect(() => {
    const stored = localStorage.getItem('sentinelx-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (stored === 'light' || stored === 'dark') {
      setTheme(stored);
    } else {
      setTheme(prefersDark ? 'dark' : 'light');
    }
    setMounted(true);
  }, [setTheme, setMounted]);

  useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
    localStorage.setItem('sentinelx-theme', theme);
  }, [theme]);

  return children;
}
