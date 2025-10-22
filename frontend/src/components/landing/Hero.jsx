import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useReport } from "../../context/ReportContext";
import apiService from "../../services/api";
import { Sparkles } from "lucide-react";
import CompanySearch from "./CompanySearch";
import "../../styles/hero.css";

const Hero = () => {
  const [companyInput, setCompanyInput] = useState("");
  const [selectedTicker, setSelectedTicker] = useState(null); // ADD THIS
  const navigate = useNavigate();
  const { setIsLoading } = useReport();

  const handleCompanySelect = (ticker, name) => {
    setCompanyInput(name); // Update display
    setSelectedTicker(ticker); // Store ticker for analysis
  };

  const handleAnalyze = async () => {
    if (!selectedTicker) {
      alert("Please select a company from the dropdown");
      return;
    }

    setIsLoading(true);
    try {
      const result = await apiService.analyzeCompany(selectedTicker);
      navigate(`/report?ticker=${result.ticker}`);
      setCompanyInput("");
      setSelectedTicker(null);
    } catch (error) {
      console.error("Error message:", error.message);

      if (!error.message.includes("HTTP")) {
        alert("Network error - check your internet or API URL");
      } else {
        alert(`Error: ${error.message}`);
      }
      alert("Error analyzing company. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="hero">
      <div className="container">
        <h1>Get an instant company evaluation!</h1>
        <p className="subtitle">
          Real-time company analysis for smarter decisions.
        </p>

        <div className="search-container">
          <CompanySearch onSelect={handleCompanySelect} />

          <button
            onClick={handleAnalyze}
            className={`analyze-button ${
              selectedTicker ? "active" : "disabled"
            }`}
            disabled={!selectedTicker}
          >
            <Sparkles size={18} />
            <span>Analyze Company</span>
          </button>
        </div>

        <p className="helper-text">
          Get a comprehensive analysis delivered to your dashboard in seconds!
        </p>
      </div>
    </section>
  );
};

export default Hero;
