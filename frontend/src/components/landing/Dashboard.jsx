import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  TrendingUp,
  Clock,
  Award,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import "../../styles/dashboard.css";
import apiService from "../../services/api";

const Dashboard = () => {
  const [companies, setCompanies] = useState([]);
  const [pagination, setPagination] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [cache, setCache] = useState({});
  const [cacheTimestamp, setCacheTimestamp] = useState({});
  const CACHE_DURATION = 5 * 60 * 1000;

  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboard(currentPage);
  }, [currentPage]);

  const fetchDashboard = async (page) => {
    try {
      setLoading(true);

      const now = Date.now();
      const cachedData = cache[page];
      const cachedTime = cacheTimestamp[page];

      if (cachedData && cachedTime && now - cachedTime < CACHE_DURATION) {
        console.log(`Using cached data for page ${page}`);
        setCompanies(cachedData.companies);
        setPagination(cachedData.pagination);
        setLoading(false);
        return;
      }

      console.log(`Fetching dashboard page ${page}...`);
      const data = await apiService.getDashboard(page);
      console.log("Dashboard data received:", data);

      setCompanies(data.companies);
      setPagination(data.pagination);

      setCache((prev) => ({ ...prev, [page]: data }));
      setCacheTimestamp((prev) => ({ ...prev, [page]: now }));
    } catch (error) {
      console.error("Failed to fetch dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCardClick = (ticker) => {
    navigate(`/report?ticker=${ticker}`);
  };

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= pagination.total_pages) {
      setCurrentPage(newPage);
      // Scroll to top of dashboard
      document
        .querySelector(".dashboard-section")
        ?.scrollIntoView({ behavior: "smooth" });
    }
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

  if (!pagination || companies.length === 0) {
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

        {/* Pagination Controls */}
        {pagination.total_pages > 1 && (
          <div className="pagination">
            <button
              className="pagination-btn"
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={currentPage === 1}
            >
              <ChevronLeft size={20} />
              Previous
            </button>

            <div className="pagination-numbers">
              {[...Array(pagination.total_pages)].map((_, index) => {
                const pageNum = index + 1;
                return (
                  <button
                    key={pageNum}
                    className={`page-number ${
                      pageNum === currentPage ? "active" : ""
                    }`}
                    onClick={() => handlePageChange(pageNum)}
                  >
                    {pageNum}
                  </button>
                );
              })}
            </div>

            <button
              className="pagination-btn"
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={currentPage === pagination.total_pages}
            >
              Next
              <ChevronRight size={20} />
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

export default Dashboard;
