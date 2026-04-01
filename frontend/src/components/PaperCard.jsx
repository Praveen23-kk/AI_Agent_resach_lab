import React from 'react';
import { Card, CardContent, Typography, Button } from '@mui/material';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

const PaperCard = ({ paper }) => {
  return (
    <Card sx={{ mb: 2, borderLeft: '4px solid #4285F4' }}>
      <CardContent>
        <Typography variant="h6" component="div" gutterBottom sx={{ fontWeight: 500, color: 'text.primary', lineHeight: 1.3 }}>
          {paper.title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          <strong>Authors:</strong> {paper.authors.join(', ')}
        </Typography>
        <Button
          variant="outlined"
          color="primary"
          size="small"
          href={paper.pdf_link}
          target="_blank"
          rel="noopener noreferrer"
          endIcon={<OpenInNewIcon />}
          sx={{ borderRadius: 16 }}
        >
          View PDF on ArXiv
        </Button>
      </CardContent>
    </Card>
  );
};

export default PaperCard;
