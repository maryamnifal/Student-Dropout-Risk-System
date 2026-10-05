/**
 * API Service for communicating with the FastAPI backend.
 * Local development base URL defaults to http://127.0.0.1:8001
 */

const API_BASE_URL = 'http://127.0.0.1:8001';

/**
 * Fetch root health and metadata.
 * @returns {Promise<Object>}
 */
export async function getRootStatus() {
  const response = await fetch(`${API_BASE_URL}/`);
  if (!response.ok) {
    throw new Error(`Failed to fetch root status: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Fetch backend health and model loading readiness.
 * @returns {Promise<Object>}
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Health check failed with status ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error('API health check error:', error);
    throw error;
  }
}

/**
 * Submit raw 52-feature student record for prediction.
 * @param {Object} studentData 52 raw student features
 * @returns {Promise<Object>} Prediction result
 */
export async function predictOutcome(studentData) {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(studentData),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.detail ||
        (errorData.errors ? JSON.stringify(errorData.errors) : `Prediction failed: ${response.status}`)
      );
    }

    return response.json();
  } catch (error) {
    console.error('API predict error:', error);
    throw error;
  }
}
