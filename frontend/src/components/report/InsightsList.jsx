import React from 'react';
import { CheckCircle, AlertCircle } from 'lucide-react';
import '../../styles/report.css';

const InsightsList = ({ greenFlags, redFlags }) => {
  return (
    <div className="insights-container">
      <h3>Market Signals</h3>
      <div className="signals-grid">
        {/* Green Flags */}
        <div className="signals-column positive">
          <h4>
            <CheckCircle size={20} />
            Positive Indicators
          </h4>
          {greenFlags && greenFlags.length > 0 ? (
            greenFlags.map((flag, index) => (
              <div key={index} className="signal-item positive">
                {flag}
              </div>
            ))
          ) : (
            <p className="no-signals">No positive signals identified</p>
          )}
        </div>

        {/* Red Flags */}
        <div className="signals-column negative">
          <h4>
            <AlertCircle size={20} />
            Risk Factors
          </h4>
          {redFlags && redFlags.length > 0 ? (
            redFlags.map((flag, index) => (
              <div key={index} className="signal-item negative">
                {flag}
              </div>
            ))
          ) : (
            <p className="no-signals">No major risks identified</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default InsightsList;