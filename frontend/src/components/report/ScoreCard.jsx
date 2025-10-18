import React from 'react';
import '../../styles/report.css';

const ScoreCard = ({ score }) => {
  return (
    <div className="score-card">
      <div className="score-display">
        <div className="score-number">{score}%</div>
        <div className="score-label">Interview Probability</div>
      </div>
    </div>
  );
};

export default ScoreCard;
