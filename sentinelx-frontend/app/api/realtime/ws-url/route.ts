import { NextResponse } from 'next/server';

import { buildWebSocketUrl } from '@/lib/server-proxy';

export function GET() {
  return NextResponse.json({ url: buildWebSocketUrl() });
}
