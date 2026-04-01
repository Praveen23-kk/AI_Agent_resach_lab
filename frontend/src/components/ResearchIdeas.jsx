import React, { useState } from 'react';
import { Lightbulb, Loader2, Sparkles, Database, Code, Target } from 'lucide-react';
import { generateResearchIdeas } from '../api/researchApi';

const ResearchIdeas = ({ topic, contextText }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [ideas, setIdeas] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    setIdeas(null);

    // If context string is too large, we cap it heuristically to save tokens
    const safeContext = contextText ? contextText.substring(0, 4000) : "No context provided.";

    try {
      const data = await generateResearchIdeas(topic, safeContext);
      if (data && data.ideas) {
        setIdeas(data.ideas);
      } else {
        throw new Error("Invalid response from server.");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="research-ideas-section" style={{ marginTop: '3rem', paddingTop: '2rem', borderTop: '2px dashed var(--border)' }}>
      <h2 className="section-title">
        <Lightbulb size={24} color="#FBBF24" />
        AI Idea Generator
      </h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
        Leverage Gemini to brainstorm novel, academic-ready research topics based on the retrieved context.
      </p>

      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <button 
          className="search-button" 
          onClick={handleGenerate} 
          disabled={isGenerating}
          style={{ display: 'inline-flex', justifyContent: 'center', background: 'linear-gradient(135deg, #10B981, #059669)' }}
        >
          {isGenerating ? <Loader2 className="spinner" size={18} style={{marginRight: '8px'}}/> : <Sparkles size={18} style={{marginRight: '8px'}}/>}
          {isGenerating ? 'Brainstorming Ideas...' : 'Generate 5 Novel Ideas'}
        </button>
      </div>

      {error && (
        <div className="error-message" style={{ padding: '1rem', marginTop: '1rem' }}>
          {error}
        </div>
      )}

      {/* Generated Ideas Result Grid */}
      {ideas && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '1rem' }}>
          {ideas.map((idea, idx) => (
            <div key={idx} className="insight-card" style={{ padding: '1.5rem', borderLeft: '4px solid #10B981' }}>
              <h3 style={{ margin: '0 0 1rem 0', color: '#F8FAFC', fontSize: '1.25rem' }}>
                <span style={{ color: '#10B981', marginRight: '8px' }}>#{idx + 1}</span>
                {idea.Title}
              </h3>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <h4 style={{ margin: '0 0 0.4rem 0', color: '#94A3B8', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Target size={14} color="#F87171" /> Problem Statement
                  </h4>
                  <p style={{ margin: 0, color: '#CBD5E1', fontSize: '0.95rem' }}>{idea.Problem_Statement}</p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '1.5rem' }}>
                  <div style={{ background: 'rgba(59, 130, 246, 0.05)', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(59, 130, 246, 0.1)' }}>
                    <h4 style={{ margin: '0 0 0.4rem 0', color: '#60A5FA', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Code size={14} color="#60A5FA" /> Proposed Method
                    </h4>
                    <p style={{ margin: 0, color: '#E2E8F0', fontSize: '0.9rem' }}>{idea.Proposed_Method}</p>
                  </div>
                  
                  <div style={{ background: 'rgba(167, 139, 250, 0.05)', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(167, 139, 250, 0.1)' }}>
                    <h4 style={{ margin: '0 0 0.4rem 0', color: '#C084FC', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Database size={14} color="#C084FC" /> Suggested Dataset
                    </h4>
                    <p style={{ margin: 0, color: '#E2E8F0', fontSize: '0.9rem' }}>{idea.Suggested_Dataset}</p>
                  </div>
                </div>

                <div style={{ borderTop: '1px dashed var(--border)', paddingTop: '1rem', marginTop: '0.5rem' }}>
                  <h4 style={{ margin: '0 0 0.4rem 0', color: '#34D399', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Sparkles size={14} color="#34D399" /> Expected Impact
                  </h4>
                  <p style={{ margin: 0, color: '#F1F5F9', fontStyle: 'italic', fontSize: '0.95rem' }}>{idea.Expected_Impact}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ResearchIdeas;
