export type RealtimeEventType =
  | 'new_signal'
  | 'new_correlated_event'
  | 'new_risk_score'
  | 'new_alert'
  | 'system_status_update';

export type RealtimePayload<T = unknown> = {
  type: RealtimeEventType;
  data: T;
};

export type WebSocketClientOptions = {
  onMessage: (event: RealtimePayload) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: () => void;
};

async function resolveWebSocketUrl(): Promise<string> {
  if (typeof window !== 'undefined') {
    try {
      const response = await fetch('/api/realtime/ws-url', { cache: 'no-store' });
      if (response.ok) {
        const data = (await response.json()) as { url?: string };
        if (data.url) {
          return data.url;
        }
      }
    } catch {
      // fall through to public env
    }
  }
  return (
    process.env.NEXT_PUBLIC_WS_URL ??
    process.env.NEXT_PUBLIC_WS_BASE_URL ??
    'ws://localhost:4000/ws'
  );
}

export async function createWebSocketClient({
  onMessage,
  onOpen,
  onClose,
  onError,
}: WebSocketClientOptions): Promise<WebSocket> {
  const url = await resolveWebSocketUrl();
  const socket = new WebSocket(url);

  socket.onopen = () => onOpen?.();
  socket.onclose = () => onClose?.();
  socket.onerror = () => onError?.();
  socket.onmessage = (message) => {
    try {
      const parsed = JSON.parse(message.data) as RealtimePayload;
      if (parsed && typeof parsed.type === 'string') {
        onMessage(parsed);
      }
    } catch {
      // ignore malformed messages
    }
  };

  return socket;
}
