import React, { useState, useEffect, useRef } from 'react';
import { Search } from 'lucide-react';
import companies from '../../data/companies.json';

const CompanySearch = ({ onSelect }) => {
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const dropdownRef = useRef(null);

  useEffect(() => {
    // Filter companies as user types
    if (input.length < 2) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }

    const query = input.toLowerCase();
    const matches = Object.entries(companies)
      .filter(([ticker, name]) => 
        ticker.toLowerCase().includes(query) || 
        name.toLowerCase().includes(query)
      )
      .slice(0, 10) // Limit to 10 results
      .map(([ticker, name]) => ({ ticker, name }));

    setSuggestions(matches);
    setShowDropdown(matches.length > 0);
  }, [input]);

  const handleSelect = (ticker, name) => {
  console.log('=== CompanySearch.handleSelect ===');
  console.log('Ticker:', ticker);
  console.log('Name:', name);
  
  setInput(`${name} (${ticker})`);
  setShowDropdown(false);
  onSelect(ticker, name);
};

  const handleKeyDown = (e) => {
    if (!showDropdown) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex(prev => 
        prev < suggestions.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
    } else if (e.key === 'Enter' && selectedIndex >= 0) {
      e.preventDefault();
      const selected = suggestions[selectedIndex];
      handleSelect(selected.ticker, selected.name);
    }
  };

  return (
    <div className="search-wrapper" ref={dropdownRef}>
      <div className="search-input-wrapper">
        <Search className="search-icon" size={20} />
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search companies (e.g., Apple, META, Tesla)"
          className="search-input"
        />
      </div>

      {showDropdown && (
        <div className="search-dropdown">
          {suggestions.map((item, index) => (
            <div
              key={item.ticker}
              className={`dropdown-item ${index === selectedIndex ? 'selected' : ''}`}
              onClick={() => handleSelect(item.ticker, item.name)}
            >
              <span className="company-name">{item.name}</span>
              <span className="company-ticker">{item.ticker}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CompanySearch;