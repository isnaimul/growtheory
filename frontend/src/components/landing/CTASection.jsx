import React from 'react';
import '../../styles/cta.css';

const CTASection = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <section className="cta-section">
      <div className="container">
        <h2>Ready to make smarter career decisions?</h2>
        <p>Join thousands of job seekers using data-driven intelligence</p>
        <button 
          className="cta-button-large"
          onClick={scrollToTop}
        >
          Analyze Your First Company
        </button>
      </div>
    </section>
  );
};

export default CTASection;
