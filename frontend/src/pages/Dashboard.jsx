import React, { useState } from 'react';
import { Container, Box, Typography, Grid, Alert } from '@mui/material';
import { runResearch } from '../api/researchApi';

import SearchBar from '../components/SearchBar';
import LoadingIndicator from '../components/LoadingIndicator';
import PaperCard from '../components/PaperCard';
import InsightsPanel from '../components/InsightsPanel';
import PaperComparison from '../components/PaperComparison';
import ResearchIdeasPanel from '../components/ResearchIdeasPanel';

const Dashboard = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const responseData = await runResearch(query);
      setResults(responseData);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 6 }}>
      {/* Header */}
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 700, color: '#4285F4' }}>
          Agentic Research Lab
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ fontWeight: 400 }}>
          AI-powered literature search, vector embedding, and RAG synthesis.
        </Typography>
      </Box>

      {/* Top Section: Search */}
      <SearchBar query={query} setQuery={setQuery} onSearch={handleSearch} disabled={isLoading} />

      {/* Loading Indicator */}
      {isLoading && <LoadingIndicator />}

      {/* Error State */}
      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {/* Middle & Lower Sections */}
      {!isLoading && !error && results && (
        <Box>
          <Grid container spacing={4}>
            {/* Left Column: Retrieved Papers */}
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <span style={{ color: '#4285F4' }}>1.</span> Retrieved Papers
              </Typography>
              {results.papers && results.papers.length > 0 ? (
                results.papers.map((paper, idx) => (
                  <PaperCard key={idx} paper={paper} />
                ))
              ) : (
                <Typography color="text.secondary">No papers retrieved.</Typography>
              )}
            </Grid>

            {/* Right Column: Insights */}
            <Grid item xs={12} md={8}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <span style={{ color: '#34A853' }}>2.</span> Research Insights
              </Typography>
              <InsightsPanel 
                summary={results.summary}
                gaps={results.research_gaps}
                future={results.future_directions}
              />
            </Grid>
          </Grid>

          {/* Lower Section 1: Paper Comparison */}
          {results.papers && results.papers.length >= 2 && (
            <PaperComparison papers={results.papers} />
          )}

          {/* Lower Section 2: Idea Generator */}
          {results.papers && results.papers.length > 0 && (
            <ResearchIdeasPanel 
              topic={query} 
              contextText={results.papers.map(p => p.abstract).join('\n\n')} 
            />
          )}
        </Box>
      )}
    </Container>
  );
};

export default Dashboard;
