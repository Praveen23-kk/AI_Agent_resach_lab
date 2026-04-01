import React from 'react';
import { Search, Loader2 } from 'lucide-react';

const SearchBox = ({ query, setQuery, onSearch, disabled }) => {
  return (
    <form onSubmit={onSearch} className="search-container">
      <input
        type="text"
        className="search-input"
        placeholder="e.g., How does multi-agent reinforcement learning improve swarm robotics?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={disabled}
      />
      <button 
        type="submit" 
        className="search-button" 
        disabled={disabled || !query.trim()}
      >
        {disabled ? <Loader2 className="spinner" size={20} /> : <Search size={20} />}
        <span>{disabled ? 'Researching...' : 'Start Research'}</span>
      </button>
    </form>
  );
};

export default SearchBox;
