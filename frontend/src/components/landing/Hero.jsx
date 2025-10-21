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
      alert("Error analyzing company. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="hero">
      <div className="container">
        <h1>Make Every Application Count</h1>
        <p className="subtitle">
          AI-powered intelligence that tells you which companies are worth your
          time
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
          Get your intelligence report in under 3 minutes
        </p>
      </div>
    </section>
  );
};

export default Hero;
