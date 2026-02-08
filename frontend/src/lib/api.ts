const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('better-auth-token');
  }
  return null;
}

export default async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const token = getAuthToken();

  // FIX: Hum TypeScript ko bata rahe hain ke ye simple object hai
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: headers,
  });

  return response;
}