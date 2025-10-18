import React from 'react';
import '../../styles/report.css';

const ReportHeader = ({ companyName, role, timestamp }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="report-header">
      <h1>{companyName}</h1>
      <p>{role || 'General Analysis'}</p>
      <p className="report-meta">Generated {formatDate(timestamp)}</p>
    </div>
  );
};

export default ReportHeader;
