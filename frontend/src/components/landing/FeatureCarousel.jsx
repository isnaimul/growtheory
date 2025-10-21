import React, { useState } from 'react';
import { Award, DollarSign, AlertTriangle, ChevronLeft, ChevronRight } from 'lucide-react';
import '../../styles/carousel.css';

const features = [
  {
    id: 1,
    icon: Award,
    title: "Instant Company Grading",
    description: "Get a clear A-F grade on every company in seconds. Know immediately if a company is worth your application based on financial health, stability, and career opportunities.",
    features: [
      "Overall health score (0-100)",
      "Letter grade for quick assessment",
      "Data-driven evaluation"
    ]
  },
  {
    id: 2,
    icon: DollarSign,
    title: "Financial Health Transparency",
    description: "See the numbers that matter. Revenue, market cap, profit margins, and employee count - understand if a company can offer job security and competitive compensation.",
    features: [
      "Real-time financial metrics",
      "Market capitalization and revenue",
      "Profitability and growth indicators"
    ]
  },
  {
    id: 3,
    icon: AlertTriangle,
    title: "Career Risk Assessment",
    description: "Make informed decisions with comprehensive pros and cons. Understand company culture, growth potential, and red flags before you invest time in an application.",
    features: [
      "Green flags and opportunities",
      "Red flags and risk factors",
      "Work culture insights"
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