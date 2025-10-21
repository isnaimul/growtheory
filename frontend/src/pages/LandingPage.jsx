import React from 'react';
import Navbar from '../components/layout/Navbar';
import Footer from '../components/layout/Footer';
import LoadingOverlay from '../components/layout/LoadingOverlay';
import Hero from '../components/landing/Hero';
import Dashboard from '../components/landing/Dashboard';
import FeatureCarousel from '../components/landing/FeatureCarousel';
import CTASection from '../components/landing/CTASection';
import Disclaimer from '../components/layout/Disclaimer';
import { useReport } from '../context/ReportContext';

const LandingPage = () => {
  const { isLoading } = useReport();

  return (
    <>
      <Navbar />
      <Hero />
      <Dashboard />
      <FeatureCarousel />
      <CTASection />
      <Disclaimer />
      <Footer />
      <LoadingOverlay isVisible={isLoading} />
    </>
  );
};

export default LandingPage;
