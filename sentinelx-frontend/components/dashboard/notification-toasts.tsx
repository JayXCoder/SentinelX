"use client";

import { useDashboardStore } from '@/stores/dashboard-store';

const toneClasses = {
  info: 'border-cyan-400/20 bg-cyan-400/10 text-cyan-100',
  success: 'border-emerald-400/20 bg-emerald-400/10 text-emerald-100',
  warning: 'border-amber-400/20 bg-amber-400/10 text-amber-100',
  critical: 'border-rose-400/20 bg-rose-400/10 text-rose-100',
};

export function NotificationToasts() {
  const notifications = useDashboardStore((state) => state.notifications);

  if (!notifications.length) return null;

  return (
    <div className="fixed right-4 top-4 z-[60] flex w-[20rem] flex-col gap-3">
      {notifications.map((notification) => (
        <div key={notification.id} className={`rounded-2xl border p-4 shadow-2xl backdrop-blur-xl ${toneClasses[notification.tone]}`}>
          <p className="text-sm font-semibold">{notification.title}</p>
          <p className="mt-1 text-sm opacity-90">{notification.body}</p>
        </div>
      ))}
    </div>
  );
}
