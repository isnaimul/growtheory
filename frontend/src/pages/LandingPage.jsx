import React from 'react';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';
import LoadingOverlay from '../components/layout/LoadingOverlay';
import Hero from '../components/landing/Hero';
import FeatureCarousel from '../components/landing/FeatureCarousel';
import CTASection from '../components/landing/CTASection';
import { useReport } from '../context/ReportContext';

const LandingPage = () => {
  const { isLoading } = useReport();

  return (
    <>
      <Navbar />
      <Hero />
      <FeatureCarousel />
      <CTASection />
      <Footer />
      <LoadingOverlay isVisible={isLoading} />
    </>
  );
};

export default LandingPage;
