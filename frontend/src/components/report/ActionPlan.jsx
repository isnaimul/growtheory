import React from 'react';
import { ChevronRight } from 'lucide-react';
import '../../styles/report.css';

const ActionPlan = ({ actionSteps }) => {
  if (!actionSteps || actionSteps.length === 0) {
    return null;
  }

  return (
    <div className="action-card">
      <h3>Your Action Plan</h3>
      <div>
        {actionSteps.map((step, index) => (
          <div key={index} className="action-step">
            <ChevronRight size={18} className="action-icon" />
            <div>
              <strong>Step {index + 1}:</strong> {step}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ActionPlan;

