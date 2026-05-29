type PageHeaderProps = {
  eyebrow: string;
  title: string;
  children?: React.ReactNode;
};

export function PageHeader({ eyebrow, title, children }: PageHeaderProps) {
  return (
    <div>
      <p className="text-sm uppercase tracking-[0.3em] text-accent">{eyebrow}</p>
      <h2 className="mt-2 font-display text-3xl text-foreground">{title}</h2>
      {children ? <div className="mt-3 max-w-2xl text-sm leading-6 text-muted">{children}</div> : null}
    </div>
  );
}

export const dashboardCardClass = 'rounded-[2rem] border border-border bg-card-solid p-6 shadow-card';
export const dashboardPanelClass = 'rounded-[1.75rem] border border-border bg-card-solid p-5 shadow-card';
export const dashboardButtonClass =
  'rounded-full border border-border bg-background px-4 py-2 text-sm text-foreground transition hover:bg-accent-soft';
