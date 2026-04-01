import React from 'react';

const LoadingSpinner = ({ message = "Agent is planning, searching ArXiv, indexing vectors, and analyzing..." }) => {
  return (
    <div className="loading-indicator">
      <div className="spinner"></div>
      <p>{message}</p>
    </div>
  );
};

export default LoadingSpinner;
