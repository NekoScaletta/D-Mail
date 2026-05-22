const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function predictEmail(text) {
  const response = await fetch(`${API_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || 'Backend không phản hồi hợp lệ.');
  }

  return data;
}
