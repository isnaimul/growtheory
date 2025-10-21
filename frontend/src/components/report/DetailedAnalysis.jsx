import React from 'react';
import '../../styles/report.css';

const DetailedAnalysis = ({ detailedAnalysis }) => {
  if (!detailedAnalysis) {
    return null;
  }

  // Format the text content properly
  const formatAnalysis = (text) => {
    // Split by lines
    const lines = text.split('\n');
    
    return lines.map((line, index) => {
      const trimmedLine = line.trim();
      
      // Skip empty lines
      if (!trimmedLine) return null;
      
      // Headers (lines ending with :)
      if (trimmedLine.endsWith(':') && !trimmedLine.includes('http')) {
        return (
          <h4 key={index} className="analysis-header">
            {trimmedLine}
          </h4>
        );
      }
      
      // Numbered lists (1. 2. 3.)
      if (/^\d+\./.test(trimmedLine)) {
        return (
          <div key={index} className="analysis-numbered-item">
            {trimmedLine}
          </div>
        );
      }
      
      // Bullet points (-, ✅, ❗, •)
      if (/^[-✅❗•]/.test(trimmedLine)) {
        const icon = trimmedLine[0];
        const content = trimmedLine.substring(1).trim();
        let className = 'analysis-bullet-item';
        
        if (icon === '✅') className += ' positive';
        if (icon === '❗') className += ' warning';
        
        return (
          <div key={index} className={className}>
            <span className="bullet-icon">{icon}</span>
            <span>{content}</span>
          </div>
        );
      }
      
      // Emojis at start (🚨, 📊, etc.)
      if (/^[\u{1F300}-\u{1F9FF}]/u.test(trimmedLine)) {
        return (
          <div key={index} className="analysis-highlight">
            {trimmedLine}
          </div>
        );
      }
      
      // Regular paragraphs
      return (
        <p key={index} className="analysis-paragraph">
          {trimmedLine}
        </p>
      );
    }).filter(Boolean); // Remove null entries
  };

  return (
    <details className="details-section">
      <summary>View Detailed Analysis</summary>
      <div className="analysis-content">
        {formatAnalysis(detailedAnalysis)}
      </div>
    </details>
  );
};

export default DetailedAnalysis;