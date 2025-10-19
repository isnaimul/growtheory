import React, { useState } from 'react';
import { Award, Target, Shield, ChevronLeft, ChevronRight } from 'lucide-react';
import '../../styles/carousel.css';

const features = [
  {
    id: 1,
    icon: Award,
    title: "Company Report Cards",
    description: "Get a comprehensive grade on every company's hiring activity. We analyze 20+ data points to give you a clear score on hiring velocity, stability, and growth.",
    features: [
      "Overall hiring velocity score (0-10)",
      "Company stability rating",
      "Interview probability for your profile"
    ]
  },
  {
    id: 2,
    icon: Target,
    title: "Hiring Signals",
    description: "See positive and negative indicators at a glance. No more guessing if a company is actually hiring or just collecting resumes.",
    features: [
      "Positive momentum indicators",
      "Risk signals and red flags",
      "Real-time hiring activity"
    ]
  },
  {
    id: 3,
    icon: Shield,
    title: "Layoff Risk Prediction",
    description: "Know before you apply. Our AI analyzes financial health, industry trends, and company signals to predict layoff risk over the next 12 months.",
    features: [
      "12-month stability forecast",
      "Financial health analysis",
      "Industry trend indicators"
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
        <h2 className="carousel-heading">Powerful Features</h2>
        
        <div className="carousel-container">
          {/* Navigation Arrows */}
          <button 
            className="carousel-nav prev" 
            onClick={prevSlide}
            aria-label="Previous feature"
          >
            <ChevronLeft size={32} />
          </button>

          {/* Main Card */}
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

          {/* Navigation Arrows */}
          <button 
            className="carousel-nav next" 
            onClick={nextSlide}
            aria-label="Next feature"
          >
            <ChevronRight size={32} />
          </button>
        </div>

        {/* Dots Indicator */}
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

        {/* Counter */}
        <div className="carousel-counter">
          {currentIndex + 1} / {features.length}
        </div>
      </div>
    </section>
  );
};

export default FeatureCarousel;
