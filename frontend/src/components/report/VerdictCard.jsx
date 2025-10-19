import React from 'react';
import { TrendingUp, Minus, TrendingDown } from 'lucide-react';
import '../../styles/report.css';

const VerdictCard = ({ verdict }) => {
  const getVerdictStyle = () => {
    const v = verdict.toUpperCase();
    if (v.includes('BULLISH') || v.includes('✅')) return { style: 'positive', icon: <TrendingUp size={24} /> };
    if (v.includes('BEARISH') || v.includes('❌')) return { style: 'negative', icon: <TrendingDown size={24} /> };
    return { style: 'neutral', icon: <Minus size={24} /> };
  };

  const { style, icon } = getVerdictStyle();

  return (
    <div className={`verdict-card ${style}`}>
      <h3>Investment Outlook</h3>
      <div className="verdict-content">
        {icon}
        <span className="verdict-text">{verdict}</span>
      </div>
    </div>
  );
};

export default VerdictCard;