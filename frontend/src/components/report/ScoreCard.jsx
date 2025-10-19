import React from 'react';
import '../../styles/report.css';

const ScoreCard = ({ score, grade }) => {
  return (
    <div className="score-card">
      <div className="score-display">
        <div className="grade-badge-large">{grade}</div>
        <div className="score-number">{score}/100</div>
        <div className="score-label">Company Health Score</div>
      </div>
    </div>
  );
};

export default ScoreCard;