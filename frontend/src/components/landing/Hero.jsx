import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useReport } from '../../context/ReportContext';
import apiService from '../../services/api';
import { Sparkles } from 'lucide-react';
import CompanySearch from './CompanySearch';
import '../../styles/hero.css';

const Hero = () => {
  const navigate = useNavigate();
  const { setIsLoading } = useReport();

  const handleCompanySelect = async (ticker, name) => {
    setIsLoading(true);

    try {
      // Call API with ticker directly
      const result = await apiService.analyzeCompany(ticker);
      
      // Navigate to report page
      navigate(`/report?ticker=${result.ticker}`);
    } catch (error) {
      alert('Error analyzing company. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="hero">
      <div className="container">
        <h1>Make Every Application Count</h1>
        <p className="subtitle">AI-powered intelligence that tells you which companies are worth your time</p>
        
        <div className="search-container">
          <CompanySearch onSelect={handleCompanySelect} />
          <button 
            className="analyze-button"
            style={{ pointerEvents: 'none', opacity: 0.6 }}
          >
            <Sparkles size={18} />
            <span>Analyze</span>
          </button>
        </div>
        
        <p className="helper-text">Get your intelligence report in under 3 minutes</p>
      </div>
    </section>
  );
};

export default Hero;