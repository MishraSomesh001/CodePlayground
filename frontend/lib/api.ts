const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface ApiError {
  detail: string;
}

/**
 * Typed wrapper around fetch for calling the FastAPI backend.
 * Runs server-side only (from NextAuth callbacks / server actions).
 */
export async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<{ data?: T; error?: string }> {
  try {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json", ...options.headers },
      ...options,
    });

    if (!res.ok) {
      const body: ApiError = await res.json().catch(() => ({ detail: "Unknown error" }));
      return { error: body.detail };
    }

    const data: T = await res.json();
    return { data };
  } catch {
    return { error: "Failed to connect to the API server." };
  }
}
