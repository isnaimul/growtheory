import React from 'react';
import '../../styles/report.css';

const InsightsList = ({ insights }) => {
  if (!insights || insights.length === 0) {
    return null;
  }

  return (
    <div className="insights-container">
      <h3>Quick Insights</h3>
      <div>
        {insights.map((insight, index) => (
          <div key={index} className={`insight-item ${insight.type}`}>
            <strong>{insight.title}</strong>
            <p>{insight.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InsightsList;
