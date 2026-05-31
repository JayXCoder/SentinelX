import { NextRequest } from 'next/server';

import { proxyToUpstream } from '@/lib/server-proxy';

type RouteContext = { params: Promise<{ path: string[] }> };

async function handle(request: NextRequest, context: RouteContext) {
  const { path } = await context.params;
  return proxyToUpstream(
    request,
    path,
    'API_INTELLIGENCE_URL',
    'NEXT_PUBLIC_INTELLIGENCE_API_URL',
  );
}

export const GET = handle;
export const POST = handle;
export const PATCH = handle;
export const PUT = handle;
export const DELETE = handle;
