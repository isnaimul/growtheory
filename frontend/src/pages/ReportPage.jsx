import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import ReportHeader from '../components/report/ReportHeader';
import ScoreCard from '../components/report/ScoreCard';
import MetricsGrid from '../components/report/MetricsGrid';
import VerdictCard from '../components/report/VerdictCard';
import InsightsList from '../components/report/InsightsList';
import ActionPlan from '../components/report/ActionPlan';
import DetailedAnalysis from '../components/report/DetailedAnalysis';
import { useReport } from '../context/ReportContext';

const ReportPage = () => {
  const navigate = useNavigate();
  const { reportData } = useReport();

  useEffect(() => {
    // If no report data, redirect back to landing page
    if (!reportData) {
      navigate('/');
    }
  }, [reportData, navigate]);

  // Show loading state while checking for data
  if (!reportData) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <Navbar showNewSearch={true} />
      <div className="report-container">
        <div className="container">
          <ReportHeader 
            companyName={reportData.company}
            role={reportData.role}
            timestamp={reportData.timestamp}
          />
          
          <ScoreCard score={reportData.score} />
          
          <MetricsGrid 
            hiringVelocity={reportData.hiringVelocity}
            stabilityScore={reportData.stabilityScore}
            layoffRisk={reportData.layoffRisk}
          />
          
          <VerdictCard verdict={reportData.verdict} />
          
          <InsightsList insights={reportData.insights} />
          
          <ActionPlan actionSteps={reportData.actionSteps} />
          
          <DetailedAnalysis detailedAnalysis={reportData.detailedAnalysis} />
        </div>
      </div>
    </>
  );
};

export default ReportPage;
