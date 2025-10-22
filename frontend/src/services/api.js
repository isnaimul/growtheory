// API Service Layer
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const ANALYZE_ENDPOINT = import.meta.env.VITE_API_ANALYZE_ENDPOINT;
const STATUS_ENDPOINT = import.meta.env.VITE_API_STATUS_ENDPOINT;

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async analyzeCompany(companyName, ticker = null) {
    try {
      const payload = {
        company: companyName,
        ticker: ticker || companyName,
      };

      const response = await fetch(`${this.baseUrl}${ANALYZE_ENDPOINT}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Status:", response.status);
        console.error("Response body:", errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error analyzing company:", error);
      throw error;
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

  async getDashboard(page = 1) {
    const url = `${this.baseUrl}/dashboard?page=${page}`;
    try {
      const response = await fetch(`${this.baseUrl}/dashboard?page=${page}`);

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

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Error fetching report:", error);
      throw error;
    }
  }

  // Mock data for testing without backend
  async getMockData(companyName) {
    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 2000));

    return {
      company: companyName,
      role: "Software Engineer",
      timestamp: new Date().toISOString(),
      score: 68,
      hiringVelocity: 8.5,
      stabilityScore: 9,
      layoffRisk: 5,
      verdict: `You're a strong candidate for ${companyName}. Your background aligns well with their hiring patterns.`,
      insights: [
        {
          type: "positive",
          title: "Strong Alumni Network",
          description: "Multiple alumni from your school work here",
        },
        {
          type: "positive",
          title: "Fresh Posting",
          description: "Job posted recently with high hiring velocity",
        },
        {
          type: "neutral",
          title: "6-Week Timeline",
          description: "Average interview process takes 42-49 days",
        },
      ],
      actionSteps: [
        "Apply on company careers page today",
        "Reach out to alumni connections",
        "Prepare for technical assessment",
        "Attend upcoming networking events",
      ],
      detailedAnalysis: "<p>Detailed analysis will go here...</p>",
    };
  }
}

export default new ApiService();
