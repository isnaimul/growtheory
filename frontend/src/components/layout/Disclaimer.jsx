import React from 'react';
import { AlertCircle } from 'lucide-react';
import '../../styles/disclaimer.css';

const Disclaimer = () => {
  return (
    <section className="disclaimer-section">
      <div className="container">
        <div className="disclaimer-content">
          <AlertCircle className="disclaimer-icon" size={24} />
          <div className="disclaimer-text">
            <p>
              <strong>Disclaimer:</strong> GrowTheory provides company analysis for informational and educational purposes only. 
              This is not financial, legal, or career advice. Our AI-powered analysis may contain errors or outdated information. 
              Company data is sourced from public APIs and third-party services, and accuracy is not guaranteed. 
              Always conduct your own research and consult with qualified professionals before making career or financial decisions. 
              GrowTheory is not liable for any decisions made based on information provided through this service.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Disclaimer;
