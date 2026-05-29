export function ErrorState({ message = 'Unable to load intelligence data.' }: { message?: string }) {
  return (
    <div className="rounded-3xl border border-rose-500/25 bg-rose-500/10 p-6 text-sm text-rose-800 dark:text-rose-100">
      {message}
    </div>
  );
}
