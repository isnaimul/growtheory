import React from 'react';
import { Clock } from 'lucide-react';
import '../../styles/report.css';

const ReportHeader = ({ companyName, ticker, timestamp }) => {
  const getTimeAgo = (dateString) => {
    const now = new Date();
    const then = new Date(dateString);
    const diffMs = now - then;
    const minutes = Math.floor(diffMs / (1000 * 60));
    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes} minute${minutes === 1 ? '' : 's'} ago`;
    if (hours < 24) return `${hours} hour${hours === 1 ? '' : 's'} ago`;
    
    const days = Math.floor(hours / 24);
    if (days === 1) return '1 day ago';
    return `${days} days ago`;
  };

  return (
    <div className="report-header">
      <h1>{companyName}</h1>
      <p className="ticker-label">{ticker}</p>
      <div className="report-meta">
        <Clock size={16} />
        <span>Last updated {getTimeAgo(timestamp)}</span>
      </div>
    </div>
  );
};

export default ReportHeader;