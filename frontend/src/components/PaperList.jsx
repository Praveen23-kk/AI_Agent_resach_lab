import React from 'react';
import { ArrowRight } from 'lucide-react';

const PaperList = ({ papers }) => {
  if (!papers || papers.length === 0) {
    return <p style={{ color: 'var(--text-muted)' }}>No papers retrieved.</p>;
  }

  return (
    <div className="paper-list">
      {papers.map((paper, idx) => (
        <div key={idx} className="paper-card">
          <h3>{paper.title}</h3>
          <p><strong>Authors:</strong> {paper.authors.join(', ')}</p>
          <a href={paper.pdf_link} target="_blank" rel="noreferrer" className="paper-link">
            View PDF on ArXiv <ArrowRight size={14} style={{ verticalAlign: 'middle', marginLeft: '4px' }} />
          </a>
        </div>
      ))}
    </div>
  );
};

export default PaperList;
