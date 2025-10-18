import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ReportProvider } from './context/ReportContext';
import LandingPage from './pages/LandingPage';
import ReportPage from './pages/ReportPage';

function App() {
  return (
    <ReportProvider>
      <Router>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/report" element={<ReportPage />} />
          <Route path="/report/:companyName" element={<ReportPage />} />
        </Routes>
      </Router>
    </ReportProvider>
  );
}

export default App;
