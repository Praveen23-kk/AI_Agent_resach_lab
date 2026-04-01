import React, { useState } from 'react';
import { Box, Card, CardContent, Typography, Select, MenuItem, FormControl, InputLabel, Button, Grid, CircularProgress, Alert } from '@mui/material';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import { comparePapers } from '../api/researchApi';

const PaperComparison = ({ papers }) => {
  const [selectedIdxA, setSelectedIdxA] = useState('');
  const [selectedIdxB, setSelectedIdxB] = useState('');
  const [isComparing, setIsComparing] = useState(false);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [error, setError] = useState(null);

  if (!papers || papers.length < 2) return null;

  const handleCompare = async () => {
    if (selectedIdxA === '' || selectedIdxB === '') {
      setError("Please select two different papers.");
      return;
    }
    if (selectedIdxA === selectedIdxB) {
      setError("Please select two distinct papers to compare.");
      return;
    }

    setIsComparing(true);
    setError(null);
    setComparisonResult(null);

    try {
      const data = await comparePapers(papers[selectedIdxA], papers[selectedIdxB]);
      setComparisonResult(data.comparison);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsComparing(false);
    }
  };

  const ResultBlock = ({ title, content, color }) => (
    <Box sx={{ mb: 2, p: 2, bgcolor: `${color}10`, borderRadius: 2, border: `1px solid ${color}30` }}>
      <Typography variant="subtitle2" sx={{ color: color, textTransform: 'uppercase', mb: 1, fontWeight: 'bold' }}>
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>{content}</Typography>
    </Box>
  );

  return (
    <Box sx={{ mt: 6, pt: 4, borderTop: '1px solid #e0e0e0' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 1 }}>
        <CompareArrowsIcon color="primary" sx={{ fontSize: 32 }} />
        <Typography variant="h5" component="h2" sx={{ fontWeight: 600 }}>
          Paper Comparison Tool
        </Typography>
      </Box>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Select two papers from your retrieved list to perform a deep semantic comparison.
      </Typography>

      <Grid container spacing={3} alignItems="center" sx={{ mb: 4 }}>
        <Grid item xs={12} md={5}>
          <FormControl fullWidth variant="outlined">
            <InputLabel>Paper A</InputLabel>
            <Select
              value={selectedIdxA}
              onChange={(e) => setSelectedIdxA(e.target.value)}
              label="Paper A"
              disabled={isComparing}
              sx={{ bgcolor: 'background.paper', borderRadius: 2 }}
            >
              {papers.map((p, i) => (
                <MenuItem key={i} value={i}>[A] {p.title.substring(0, 60)}...</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={2} sx={{ textAlign: 'center' }}>
          <Typography variant="subtitle1" color="text.secondary" fontWeight="bold">VS</Typography>
        </Grid>
        
        <Grid item xs={12} md={5}>
          <FormControl fullWidth variant="outlined">
            <InputLabel>Paper B</InputLabel>
            <Select
              value={selectedIdxB}
              onChange={(e) => setSelectedIdxB(e.target.value)}
              label="Paper B"
              disabled={isComparing}
              sx={{ bgcolor: 'background.paper', borderRadius: 2 }}
            >
              {papers.map((p, i) => (
                <MenuItem key={i} value={i}>[B] {p.title.substring(0, 60)}...</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleCompare}
          disabled={isComparing}
          startIcon={isComparing ? <CircularProgress size={20} color="inherit" /> : <CompareArrowsIcon />}
          sx={{ px: 4, py: 1.5 }}
        >
          {isComparing ? 'Analyzing Differences...' : 'Compare Selected Papers'}
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 4 }}>{error}</Alert>}

      {comparisonResult && (
        <Card sx={{ mt: 2, borderTop: '4px solid #4285F4' }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h6" gutterBottom sx={{ borderBottom: '1px solid #eee', pb: 2, mb: 3 }}>
              Comparative Analysis
            </Typography>
            
            <ResultBlock title="Methodology Differences" content={comparisonResult.methodology_differences} color="#4285F4" />
            <ResultBlock title="Datasets & Environments" content={comparisonResult.datasets_used} color="#34A853" />
            <ResultBlock title="Key Contributions" content={comparisonResult.key_contributions} color="#FBBC05" />
            
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12} md={6}>
                <ResultBlock title="Strengths of Each" content={comparisonResult.strengths_of_each} color="#34A853" />
              </Grid>
              <Grid item xs={12} md={6}>
                <ResultBlock title="Limitations" content={comparisonResult.limitations} color="#EA4335" />
              </Grid>
            </Grid>
            
            <Box sx={{ mt: 3 }}>
              <ResultBlock title="When to Use Paper A vs B" content={comparisonResult.when_to_use_a_vs_b} color="#4285F4" />
            </Box>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default PaperComparison;
