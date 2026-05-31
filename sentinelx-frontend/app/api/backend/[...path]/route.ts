import { NextRequest } from 'next/server';

import { proxyToUpstream } from '@/lib/server-proxy';

type RouteContext = { params: Promise<{ path: string[] }> };

async function handle(request: NextRequest, context: RouteContext) {
  const { path } = await context.params;
  return proxyToUpstream(request, path, 'API_BACKEND_URL', 'NEXT_PUBLIC_API_BASE_URL');
}

export const GET = handle;
export const POST = handle;
export const PATCH = handle;
export const PUT = handle;
export const DELETE = handle;
