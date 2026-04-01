import React from 'react';
import { BookOpen } from 'lucide-react';
import PaperList from './PaperList';
import InsightsPanel from './InsightsPanel';

const ResultsPanel = ({ results }) => {
  if (!results) return null;

  return (
    <div className="results-grid">
      
      {/* Left Column: Retrieved Papers */}
      <div className="papers-column">
        <h2 className="section-title">
          <BookOpen size={24} color="#60a5fa" />
          1. Retrieved Papers
        </h2>
        
        <PaperList papers={results.papers} />
      </div>

      {/* Right Column: AI Generated Insights */}
      <div className="insights-column">
        <InsightsPanel 
          summary={results.summary}
          gaps={results.research_gaps}
          future={results.future_directions}
        />
      </div>
      
    </div>
  );
};

export default ResultsPanel;
