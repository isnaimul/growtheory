import React from 'react';
import '../../styles/report.css';

const VerdictCard = ({ verdict }) => {
  return (
    <div className="verdict-card">
      <h3>The Verdict</h3>
      <p>{verdict}</p>
    </div>
  );
};

export default VerdictCard;
