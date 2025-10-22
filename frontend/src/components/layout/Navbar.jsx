import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/navbar.css';

const Navbar = ({ showNewSearch = false }) => {
  const navigate = useNavigate();

  const handleNavigation = () => {
    navigate('/');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <nav className="navbar">
      <div className="container">
        <div 
          className="logo"
          onClick={handleNavigation}
          style={{ cursor: 'pointer' }}
        >
          GrowTheory
        </div>
        {showNewSearch ? (
          <button 
            className="cta-button"
            onClick={handleNavigation}
          >
            New Search
          </button>
        ) : (
          <button 
            className="cta-button"
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          >
            Get Started
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;