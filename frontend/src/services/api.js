// API Service Layer
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const ANALYZE_ENDPOINT = import.meta.env.VITE_API_ANALYZE_ENDPOINT;
const STATUS_ENDPOINT = import.meta.env.VITE_API_STATUS_ENDPOINT;

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async analyzeCompany(companyName) {
    try {
      const response = await fetch(`${this.baseUrl}${ANALYZE_ENDPOINT}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          company: companyName,
        }),
      });

      const data = await response.json();

      // Handle 404 or error responses
      if (!response.ok) {
        const errorMessage = data.error || `Failed to analyze company: ${response.status}`;
        throw new Error(errorMessage);
      }

      // Check if the response indicates company not found
      if (data.error) {
        throw new Error(data.error);
      }

      // Validate we got actual data back
      if (!data.company || !data.score) {
        throw new Error("Invalid response from server - missing required data");
      }

      return data;
    } catch (error) {
      console.error("Error analyzing company:", error);
      // Re-throw with clear message
      throw new Error(error.message || "Unable to analyze company. Please check the company name and try again.");
    }
  }

  async checkStatus() {
    try {
      const response = await fetch(`${this.baseUrl}${STATUS_ENDPOINT}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error checking status:", error);
      throw error;
    }
  }

  async getDashboard() {
    try {
      const response = await fetch(`${this.baseUrl}/dashboard`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching dashboard:", error);
      throw error;
    }
  }

  async getReport(ticker) {
    try {
      const response = await fetch(`${this.baseUrl}/report?ticker=${ticker}`);

      const data = await response.json();

      if (!response.ok) {
        const errorMessage = data.error || `Report not found for ${ticker}`;
        throw new Error(errorMessage);
      }

      // Validate report data
      if (!data.company || !data.score) {
        throw new Error("Invalid report data received");
      }

      return data;
    } catch (error) {
      console.error("Error fetching report:", error);
      throw new Error(error.message || "Unable to load report. Please try again.");
    }
  }

  // REMOVED getMockData() - no more mock data!
}

export default new ApiService();
