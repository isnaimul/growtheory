import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useReport } from '../../context/ReportContext';
import apiService from '../../services/api';
import { Search, Sparkles } from 'lucide-react';
import '../../styles/hero.css';

const Hero = () => {
  const [companyInput, setCompanyInput] = useState('');
  const navigate = useNavigate();
  const { setReportData, setIsLoading } = useReport();

  const handleAnalyze = async () => {
    const company = companyInput.trim();
    
    if (!company) {
      alert('Please enter a company name');
      return;
    }

    setIsLoading(true);

    try {
      // Force mock data for debugging
      const result = await apiService.getMockData(company);
      // const result = await apiService.analyzeCompany(company);
      
      setReportData(result);
      navigate('/report');
    } catch (error) {
      alert('Error analyzing company. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleAnalyze();
    }
  };

  return (
    <section className="hero">
      <div className="container">
        <h1>Make Every Application Count</h1>
        <p className="subtitle">AI-powered intelligence that tells you which companies are worth your time</p>
        
        <div className="search-container">
          <div className="search-input-wrapper">
            <Search className="search-icon" size={20} />
            <input 
              type="text" 
              value={companyInput}
              onChange={(e) => setCompanyInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter company name (e.g., Stripe, Google, Airbnb)"
              className="search-input"
            />
          </div>
          <button 
            onClick={handleAnalyze}
            className="analyze-button"
          >
            <Sparkles size={18} />
            <span>Analyze Company</span>
          </button>
        </div>
        
        <p className="helper-text">Get your intelligence report in under 3 minutes</p>
      </div>
    </section>
  );
};

export default Hero;
