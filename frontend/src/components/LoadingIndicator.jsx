import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

const LoadingIndicator = ({ message = "Agent is planning, searching ArXiv, indexing vectors, and analyzing..." }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', py: 8 }}>
      <CircularProgress size={48} thickness={4} color="primary" sx={{ mb: 2 }} />
      <Typography variant="body1" color="text.secondary">
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingIndicator;
