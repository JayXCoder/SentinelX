import { NextRequest, NextResponse } from 'next/server';

function upstreamBase(envVar: string, publicFallback: string): string {
  return (
    process.env[envVar] ??
    process.env[publicFallback] ??
    (envVar === 'API_BACKEND_URL' ? 'http://localhost:4000' : 'http://localhost:4001')
  );
}

function apiKeyHeader(): Record<string, string> {
  const key = process.env.SENTINELX_API_KEY ?? process.env.API_KEY;
  return key ? { 'X-API-Key': key } : {};
}

export async function proxyToUpstream(
  request: NextRequest,
  pathSegments: string[],
  upstreamEnv: 'API_BACKEND_URL' | 'API_INTELLIGENCE_URL',
  publicFallback: 'NEXT_PUBLIC_API_BASE_URL' | 'NEXT_PUBLIC_INTELLIGENCE_API_URL',
): Promise<NextResponse> {
  const base = upstreamBase(upstreamEnv, publicFallback).replace(/\/$/, '');
  const path = pathSegments.join('/');
  const url = new URL(`${base}/${path}`);
  request.nextUrl.searchParams.forEach((value, key) => {
    url.searchParams.set(key, value);
  });

  const headers = new Headers(request.headers);
  headers.delete('host');
  Object.entries(apiKeyHeader()).forEach(([key, value]) => headers.set(key, value));

  const init: RequestInit = {
    method: request.method,
    headers,
    cache: 'no-store',
  };

  if (request.method !== 'GET' && request.method !== 'HEAD') {
    init.body = await request.text();
  }

  const response = await fetch(url.toString(), init);
  const body = await response.arrayBuffer();
  return new NextResponse(body, {
    status: response.status,
    headers: {
      'Content-Type': response.headers.get('Content-Type') ?? 'application/json',
    },
  });
}

function resolvePublicWebSocketBase(): string {
  const explicit =
    process.env.PUBLIC_WS_URL ??
    process.env.NEXT_PUBLIC_WS_URL ??
    '';
  if (explicit) {
    const trimmed = explicit.replace(/\/ws\/?$/, '').replace(/\/$/, '');
    return trimmed.replace(/^http/i, 'ws');
  }
  const base =
    process.env.API_BACKEND_URL ??
    process.env.NEXT_PUBLIC_API_BASE_URL ??
    'http://localhost:4000';
  return base.replace(/^http/i, 'ws').replace(/\/$/, '');
}

export function buildWebSocketUrl(): string {
  const wsBase = resolvePublicWebSocketBase();
  const key = process.env.SENTINELX_API_KEY ?? process.env.API_KEY;
  const url = `${wsBase}/ws`;
  if (!key) {
    return url;
  }
  return `${url}?api_key=${encodeURIComponent(key)}`;
}
