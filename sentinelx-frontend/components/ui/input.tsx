import { cn } from '@/lib/utils';

type InputProps = React.InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
};

export function Input({ label, className, id, ...props }: InputProps) {
  const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <label className="block space-y-2 text-sm">
      {label ? <span className="font-medium text-foreground">{label}</span> : null}
      <input
        id={inputId}
        className={cn(
          'w-full rounded-2xl border border-border bg-background px-4 py-3 text-foreground placeholder:text-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent',
          className,
        )}
        {...props}
      />
    </label>
  );
}
