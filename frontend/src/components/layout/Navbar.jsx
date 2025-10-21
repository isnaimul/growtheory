import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/navbar.css';

const Navbar = ({ showNewSearch = false }) => {
  const navigate = useNavigate();

  return (
    <nav className="navbar">
      <div className="container">
        <div 
          className="logo"
          onClick={() => navigate('/')}
          style={{ cursor: 'pointer' }}
        >
          GrowTheory
        </div>
        {showNewSearch ? (
          <button 
            className="cta-button"
            onClick={() => navigate('/')}
          >
            New Search
          </button>
        ) : (
          <button className="cta-button">
            Get Started
          </button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
