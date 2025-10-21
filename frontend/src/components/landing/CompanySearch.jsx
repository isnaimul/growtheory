import React, { useState, useEffect, useRef } from "react";
import { Search } from "lucide-react";
import companies from "../../data/companies.json";

const CompanySearch = ({ onSelect }) => {
  const [input, setInput] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const dropdownRef = useRef(null);

  useEffect(() => {
    if (input.length < 2) {
      setSuggestions([]);
      setShowDropdown(false);
      return;
    }

    const query = input.toLowerCase();
    const matches = Object.entries(companies)
      .filter(([ticker, aliases]) => {
        // Check if ticker matches
        if (ticker.toLowerCase().includes(query)) return true;

        // Check if any alias matches
        return aliases.some((alias) => alias.toLowerCase().includes(query));
      })
      .slice(0, 10)
      .map(([ticker, aliases]) => ({
        ticker,
        name: aliases[0], // Use first alias as display name
      }));

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
    if (e.key === "Enter") {
      e.preventDefault();

      if (showDropdown && selectedIndex >= 0) {
        // User selected from dropdown
        const selected = suggestions[selectedIndex];
        handleSelect(selected.ticker, selected.name);
      } else if (showDropdown && suggestions.length === 1) {
        // Only one match - auto-select it
        handleSelect(suggestions[0].ticker, suggestions[0].name);
      } else {
        // Manual entry - validate it's a ticker format
        const tickerInput = input.trim().toUpperCase();
        if (/^[A-Z]{1,5}$/.test(tickerInput)) {
          handleSelect(tickerInput, tickerInput);
        } else {
          alert(
            "Please select from dropdown or enter a valid ticker (e.g., AAPL)"
          );
        }
      }
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
              className={`dropdown-item ${
                index === selectedIndex ? "selected" : ""
              }`}
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
