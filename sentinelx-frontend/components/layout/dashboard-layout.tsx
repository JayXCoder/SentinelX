import { DashboardShell } from './dashboard-shell';

export function DashboardLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="min-h-dvh bg-background text-foreground">
      <DashboardShell>{children}</DashboardShell>
    </div>
  );
}
