import React, { useState } from 'react';
import { Award, DollarSign, AlertTriangle, ChevronLeft, ChevronRight } from 'lucide-react';
import '../../styles/carousel.css';

const features = [
  {
    id: 1,
    icon: Award,
    title: "Professional Report Cards",
    description: "Get comprehensive company analysis in seconds. Whether you're job hunting or investing, see financial health, market sentiment, and growth signals synthesized into clear, actionable intelligence.",
    features: [
      "Overall assessment score (0-10)",
      "Investment recommendations (Bullish/Neutral/Bearish)",
      "Data-driven evaluation from multiple sources"
    ]
  },
  {
    id: 2,
    icon: DollarSign,
    title: "Real-Time Financial Intelligence",
    description: "See the metrics that matter: Revenue, Market Cap, profit margins, employee count, and market sentiment - all pulled from live financial data sources.",
    features: [
      "Live financial metrics and profitability",
      "Market capitalization and growth indicators",
      "News sentiment and market positioning"
    ]
  },
  {
    id: 3,
    icon: AlertTriangle,
    title: "Dual-Perspective Analysis",
    description: "Make informed decisions with insights tailored to your needs. See hiring signals and career opportunities if you're job seeking, or investment outlook and risk factors if you're analyzing stocks.",
    features: [
      "Green flags: Growth opportunities and strengths",
      "Red flags: Risk factors and considerations",
      "Career outlook or investment recommendations"
    ]
  }
];

const FeatureCarousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev + 1) % features.length);
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev - 1 + features.length) % features.length);
  };

  const goToSlide = (index) => {
    setCurrentIndex(index);
  };

  const currentFeature = features[currentIndex];
  const IconComponent = currentFeature.icon;

  return (
    <section className="feature-carousel-section">
      <div className="container">
        <h2 className="carousel-heading">What You Get</h2>
        
        <div className="carousel-container">
          <button 
            className="carousel-nav prev" 
            onClick={prevSlide}
            aria-label="Previous feature"
          >
            <ChevronLeft size={32} />
          </button>

          <div className="carousel-card-wrapper">
            <div className="carousel-card" key={currentFeature.id}>
              <div className="carousel-icon-wrapper">
                <IconComponent size={64} className="carousel-icon" />
              </div>
              
              <h3 className="carousel-title">{currentFeature.title}</h3>
              
              <p className="carousel-description">{currentFeature.description}</p>
              
              <ul className="carousel-features">
                {currentFeature.features.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
            </div>
          </div>

          <button 
            className="carousel-nav next" 
            onClick={nextSlide}
            aria-label="Next feature"
          >
            <ChevronRight size={32} />
          </button>
        </div>

        <div className="carousel-dots">
          {features.map((_, index) => (
            <button
              key={index}
              className={`dot ${index === currentIndex ? 'active' : ''}`}
              onClick={() => goToSlide(index)}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>

        <div className="carousel-counter">
          {currentIndex + 1} / {features.length}
        </div>
      </div>
    </section>
  );
};

export default FeatureCarousel;