import React from 'react';
import { TrendingUp, Building2, AlertTriangle } from 'lucide-react';
import '../../styles/report.css';

const MetricsGrid = ({ hiringVelocity, stabilityScore, layoffRisk }) => {
  return (
    <div className="metrics-grid">
      <div className="metric-box">
        <TrendingUp className="metric-icon" size={32} />
        <div className="metric-value">{hiringVelocity}/10</div>
        <div className="metric-label">Hiring Velocity</div>
      </div>
      <div className="metric-box">
        <Building2 className="metric-icon" size={32} />
        <div className="metric-value">{stabilityScore}/10</div>
        <div className="metric-label">Company Stability</div>
      </div>
      <div className="metric-box">
        <AlertTriangle className="metric-icon" size={32} />
        <div className="metric-value">{layoffRisk}%</div>
        <div className="metric-label">Layoff Risk</div>
      </div>
    </div>
  );
};

export default MetricsGrid;
