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
  console.log('=== Hero.handleCompanySelect ===');
  console.log('Received ticker:', ticker);
  console.log('Received name:', name);
  
  setIsLoading(true);

  try {
    console.log('Calling apiService.analyzeCompany with:', name, ticker);
    const result = await apiService.analyzeCompany(name, ticker);
    console.log('API result:', result);
    
    navigate(`/report?ticker=${result.ticker}`);
  } catch (error) {
    console.log('=== ERROR CAUGHT ===');
    console.error('Full error object:', error);
    console.error('Error message:', error.message);
    alert('Error analyzing company. Please try again.');
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