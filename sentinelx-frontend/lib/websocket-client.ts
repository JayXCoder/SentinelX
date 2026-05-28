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

export function createWebSocketClient(onMessage: (event: RealtimePayload) => void) {
  const url =
    process.env.NEXT_PUBLIC_WS_URL ??
    process.env.NEXT_PUBLIC_WS_BASE_URL ??
    'ws://localhost:4000/ws';

  try {
    const socket = new WebSocket(url);
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
  } catch {
    return { close() {} } as WebSocket;
  }
}
