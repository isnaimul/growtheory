import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import ReportHeader from '../components/report/ReportHeader';
import ScoreCard from '../components/report/ScoreCard';
import MetricsGrid from '../components/report/MetricsGrid';
import VerdictCard from '../components/report/VerdictCard';
import InsightsList from '../components/report/InsightsList';
import DetailedAnalysis from '../components/report/DetailedAnalysis';
import apiService from '../services/api';

const ReportPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const ticker = searchParams.get('ticker');
  
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!ticker) {
      navigate('/');
      return;
    }

    fetchReport();
  }, [ticker, navigate]);

  const fetchReport = async () => {
    try {
      setLoading(true);
      const data = await apiService.getReport(ticker);
      
      // Parse the full_analysis to extract structured data
      const parsedData = parseAnalysis(data);
      setReportData(parsedData);
    } catch (err) {
      console.error('Error fetching report:', err);
      setError('Failed to load report');
    } finally {
      setLoading(false);
    }
  };

const parseAnalysis = (data) => {
  // Use financialData from API if available (new structured format)
  const financialData = data.financialData || null;
  
  const analysis = data.detailedAnalysis || data.full_analysis || '';
  
  // Extract green flags - looking for "🟢 Why Join:" section
  const greenMatch = analysis.match(/🟢\s*Why Join:([\s\S]*?)(?=🔴|Work Environment|Career Outlook|Recommendation|$)/i);
  const greenFlags = greenMatch 
    ? greenMatch[1].split('\n').filter(l => l.trim().startsWith('-')).map(l => l.replace(/^-\s*/, '').trim())
    : [];
  
  // Extract red flags - looking for "🔴 Considerations:" section
  const redMatch = analysis.match(/🔴\s*Considerations:([\s\S]*?)(?=Work Environment|Career Outlook|Recommendation|$)/i);
  const redFlags = redMatch
    ? redMatch[1].split('\n').filter(l => l.trim().startsWith('-')).map(l => l.replace(/^-\s*/, '').trim())
    : [];
  
  // Extract recommendation/verdict
  const verdictMatch = analysis.match(/Recommendation:\s*(.+?)(?:\n|$)/i);
  const verdict = verdictMatch ? verdictMatch[1].trim() : 'MODERATE';
  
  return {
    company: data.company,
    ticker: data.ticker || data.display_ticker,
    score: data.score,
    grade: data.grade,
    timestamp: data.timestamp,
    recommendation: verdict,
    greenFlags: greenFlags.length > 0 ? greenFlags : ['Strong market position', 'Growth potential'],
    redFlags: redFlags.length > 0 ? redFlags : ['Market volatility', 'Competition'],
    financialData: financialData,
    detailedAnalysis: analysis
  };
};

  if (loading) {
    return (
      <>
        <Navbar showNewSearch={true} />
        <div className="report-container">
          <div className="container">
            <div className="loading-state">Loading report...</div>
          </div>
        </div>
      </>
    );
  }

  if (error || !reportData) {
    return (
      <>
        <Navbar showNewSearch={true} />
        <div className="report-container">
          <div className="container">
            <div className="error-state">{error || 'Report not found'}</div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar showNewSearch={true} />
      <div className="report-container">
        <div className="container">
          <ReportHeader 
            companyName={reportData.company}
            ticker={reportData.ticker}
            timestamp={reportData.timestamp}
          />
          
          <ScoreCard 
            score={reportData.score} 
            grade={reportData.grade}
          />
          
          <VerdictCard verdict={reportData.recommendation} />
          
          <MetricsGrid financialData={reportData.financialData} />
          
          <InsightsList 
            greenFlags={reportData.greenFlags}
            redFlags={reportData.redFlags}
          />
          
          <DetailedAnalysis detailedAnalysis={reportData.detailedAnalysis} />
        </div>
      </div>
    </>
  );
};

export default ReportPage;