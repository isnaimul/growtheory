import React, { useEffect, useState } from 'react';
import '../../styles/loading.css';

const LoadingOverlay = ({ isVisible }) => {
  const [logs, setLogs] = useState([]);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!isVisible) return;

    // Fake console logs to simulate report generation
    const messages = [
      "Connecting to server...",
      "Fetching financial data...",
      "Cleaning missing values...",
      "Running sentiment analysis...",
      "Generating insights...",
      "Finalizing your report..."
    ];

    let i = 0;
    const logInterval = setInterval(() => {
      if (i < messages.length) {
        setLogs(prev => [...prev, messages[i++]]);
      } else {
        clearInterval(logInterval);
      }
    }, 2000);

    // Fake progress bar
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev < 95) return prev + Math.random() * 5;
        clearInterval(progressInterval);
        return prev;
      });
    }, 500);

    return () => {
      clearInterval(logInterval);
      clearInterval(progressInterval);
    };
  }, [isVisible]);

  if (!isVisible) return null;

  return (
    <div className="loading-overlay">
      <div className="loading-content">
        <div className="spinner"></div>
        <p className="loading-title">Generating your custom report...</p>

        {/* Skeleton shimmer placeholders */}
        <div className="skeleton-container">
          <div className="skeleton" style={{ width: '70%' }}></div>
          <div className="skeleton" style={{ width: '90%' }}></div>
          <div className="skeleton" style={{ width: '50%' }}></div>
        </div>

        {/* Console logs */}
        <div className="loading-logs">
          {logs.map((log, index) => (
            <p key={index} className="log-line">{`> ${log}`}</p>
          ))}
        </div>

        {/* Progress bar */}
        <div className="progress-bar-container">
          <div className="progress-bar" style={{ width: `${progress}%` }}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingOverlay;