import React from 'react';
import '../../styles/loading.css';

const LoadingOverlay = ({ isVisible }) => {
  if (!isVisible) return null;

  return (
    <div className="loading-overlay">
      <div className="loading-content">
        <div className="spinner"></div>
        <p>Analyzing company...</p>
        <p className="loading-detail">This takes about 2-3 minutes</p>
      </div>
    </div>
  );
};

export default LoadingOverlay;
