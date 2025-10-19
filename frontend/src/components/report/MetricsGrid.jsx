import React from 'react';
import { DollarSign, TrendingUp, Users, Building2 } from 'lucide-react';
import '../../styles/report.css';

const MetricsGrid = ({ financialData }) => {
  // Helper to format large numbers
  const formatNumber = (num) => {
    if (!num) return 'N/A';
    if (num >= 1e12) return `$${(num / 1e12).toFixed(2)}T`;
    if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
    return num.toLocaleString();
  };

  const formatPercent = (num) => {
    if (!num && num !== 0) return 'N/A';
    return `${num.toFixed(2)}%`;
  };

  return (
    <div className="metrics-grid">
      <div className="metric-box">
        <DollarSign className="metric-icon" size={32} />
        <div className="metric-value">{formatNumber(financialData?.revenue)}</div>
        <div className="metric-label">Annual Revenue</div>
      </div>
      
      <div className="metric-box">
        <Building2 className="metric-icon" size={32} />
        <div className="metric-value">{formatNumber(financialData?.market_cap)}</div>
        <div className="metric-label">Market Cap</div>
      </div>
      
      <div className="metric-box">
        <TrendingUp className="metric-icon" size={32} />
        <div className="metric-value">{formatPercent(financialData?.profit_margin)}</div>
        <div className="metric-label">Profit Margin</div>
      </div>
      
      <div className="metric-box">
        <Users className="metric-icon" size={32} />
        <div className="metric-value">{financialData?.employees?.toLocaleString() || 'N/A'}</div>
        <div className="metric-label">Employees</div>
      </div>
    </div>
  );
};

export default MetricsGrid;