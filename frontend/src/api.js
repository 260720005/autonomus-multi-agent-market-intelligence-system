const API_BASE_URL = "http://127.0.0.1:8000";

export async function generateResearchReport(query) {
  const response = await fetch(`${API_BASE_URL}/research`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      query: query,
    }),
  });

  if (!response.ok) {
    let errorMessage = "Research request failed.";

    try {
      const errorData = await response.json();

      if (errorData?.detail) {
        errorMessage = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(errorMessage);
  }

  return await response.json();
}
