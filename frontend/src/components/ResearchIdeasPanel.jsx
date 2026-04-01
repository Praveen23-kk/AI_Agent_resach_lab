import React, { useState } from 'react';
import { Box, Typography, Button, CircularProgress, Alert, Card, CardContent, Grid } from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ConstructionIcon from '@mui/icons-material/Construction';
import DatasetIcon from '@mui/icons-material/Dataset';
import InsightsIcon from '@mui/icons-material/Insights';
import { generateResearchIdeas } from '../api/researchApi';

const ResearchIdeasPanel = ({ topic, contextText }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [ideas, setIdeas] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    setIdeas(null);

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
    <Box sx={{ mt: 6, pt: 4, borderTop: '1px solid #e0e0e0', mb: 8 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 1 }}>
        <AutoAwesomeIcon sx={{ color: '#FBBC05', fontSize: 32 }} />
        <Typography variant="h5" component="h2" sx={{ fontWeight: 600 }}>
          AI Research Idea Generator
        </Typography>
      </Box>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Leverage Gemini to brainstorm novel, academic-ready research topics based on the retrieved context.
      </Typography>

      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Button
          variant="contained"
          onClick={handleGenerate}
          disabled={isGenerating}
          startIcon={isGenerating ? <CircularProgress size={20} color="inherit" /> : <AutoAwesomeIcon />}
          sx={{ px: 4, py: 1.5, bgcolor: '#34A853', '&:hover': { bgcolor: '#2e9347' }, color: '#fff' }}
        >
          {isGenerating ? 'Brainstorming Ideas...' : 'Generate 5 Novel Ideas'}
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 4 }}>{error}</Alert>}

      {ideas && (
        <Grid container spacing={3}>
          {ideas.map((idea, idx) => (
            <Grid item xs={12} key={idx}>
              <Card sx={{ borderLeft: '4px solid #34A853' }}>
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h6" sx={{ color: 'text.primary', fontWeight: 600, mb: 3 }}>
                    <span style={{ color: '#34A853', marginRight: '8px' }}>#{idx + 1}</span>
                    {idea.Title}
                  </Typography>

                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                    <Box>
                      <Typography variant="overline" sx={{ color: '#EA4335', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <InsightsIcon fontSize="small" /> Problem Statement
                      </Typography>
                      <Typography variant="body2" color="text.secondary">{idea.Problem_Statement}</Typography>
                    </Box>

                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <Box sx={{ p: 2, bgcolor: '#4285F410', borderRadius: 2 }}>
                          <Typography variant="overline" sx={{ color: '#4285F4', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            <ConstructionIcon fontSize="small" /> Proposed Method
                          </Typography>
                          <Typography variant="body2" color="text.secondary">{idea.Proposed_Method}</Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <Box sx={{ p: 2, bgcolor: '#FBBC0510', borderRadius: 2 }}>
                          <Typography variant="overline" sx={{ color: '#F9AB00', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            <DatasetIcon fontSize="small" /> Suggested Dataset
                          </Typography>
                          <Typography variant="body2" color="text.secondary">{idea.Suggested_Dataset}</Typography>
                        </Box>
                      </Grid>
                    </Grid>

                    <Box sx={{ pt: 2, borderTop: '1px dashed #e0e0e0' }}>
                      <Typography variant="overline" sx={{ color: '#34A853', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <AutoAwesomeIcon fontSize="small" /> Expected Impact
                      </Typography>
                      <Typography variant="body2" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>{idea.Expected_Impact}</Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default ResearchIdeasPanel;
