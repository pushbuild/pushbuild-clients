export declare class PushbuildError extends Error { status: number; }
export declare class Pushbuild {
  constructor(apiKey?: string, options?: { baseUrl?: string; timeoutMs?: number });
  last: { count?: number; truncated?: boolean; seconds?: number };
  apis(): Promise<string[]>;
  openapi(slug: string): Promise<Record<string, unknown>>;
  run<T = Record<string, unknown>>(slug: string, input?: Record<string, unknown>): Promise<T[]>;
}
