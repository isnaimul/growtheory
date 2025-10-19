import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { TrendingUp, Clock, Award } from "lucide-react";
import "../../styles/dashboard.css";
import apiService from "../../services/api";

console.log("API Base URL:", import.meta.env.VITE_API_BASE_URL);
console.log(
  "Full Dashboard URL:",
  `${import.meta.env.VITE_API_BASE_URL}/dashboard`
);

const Dashboard = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      console.log("Fetching dashboard...");
      const data = await apiService.getDashboard();
      console.log("Dashboard data received:", data);
      setCompanies(data);
    } catch (error) {
      console.error("Failed to fetch dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCardClick = (ticker) => {
    navigate(`/report?ticker=${ticker}`);
  };

  const getTimeAgo = (timestamp) => {
    const now = new Date();
    const then = new Date(timestamp);
    const hours = Math.floor((now - then) / (1000 * 60 * 60));

    if (hours < 1) return "Just now";
    if (hours === 1) return "1 hour ago";
    if (hours < 24) return `${hours} hours ago`;
    const days = Math.floor(hours / 24);
    if (days === 1) return "1 day ago";
    return `${days} days ago`;
  };

  const getGradeColor = (grade) => {
    if (grade.startsWith("A")) return "grade-a";
    if (grade.startsWith("B")) return "grade-b";
    if (grade.startsWith("C")) return "grade-c";
    return "grade-d";
  };

  if (loading) {
    return (
      <section className="dashboard-section">
        <div className="container">
          <h2 className="dashboard-title">Recently Analyzed Companies</h2>
          <div className="loading-state">Loading dashboard...</div>
        </div>
      </section>
    );
  }

  if (companies.length === 0) {
    return (
      <section className="dashboard-section">
        <div className="container">
          <h2 className="dashboard-title">Recently Analyzed Companies</h2>
          <p className="empty-state">
            No companies analyzed yet. Search above to get started!
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="dashboard-section">
      <div className="container">
        <h2 className="dashboard-title">Recently Analyzed Companies</h2>
        <div className="dashboard-grid">
          {companies.map((company, index) => (
            <div
              key={company.ticker}
              className="company-card"
              onClick={() => handleCardClick(company.ticker)}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="card-header">
                <h3 className="company-name">{company.company}</h3>
                <div className={`grade-badge ${getGradeColor(company.grade)}`}>
                  {company.grade}
                </div>
              </div>

              <div className="card-stats">
                <div className="stat">
                  <Award size={16} />
                  <span>{company.score}/100</span>
                </div>
                <div className="stat">
                  <Clock size={16} />
                  <span>{getTimeAgo(company.timestamp)}</span>
                </div>
              </div>

              <div className="card-footer">
                <TrendingUp size={14} />
                <span>View Full Report</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Dashboard;
