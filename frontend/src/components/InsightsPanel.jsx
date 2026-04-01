import React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ExploreIcon from '@mui/icons-material/Explore';
import ReactMarkdown from 'react-markdown';

const InsightSection = ({ title, content, icon, color }) => (
  <Card sx={{ mb: 3 }}>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 1 }}>
        {React.cloneElement(icon, { sx: { color: color, fontSize: 28 } })}
        <Typography variant="h6" sx={{ fontWeight: 600, color: 'text.primary' }}>
          {title}
        </Typography>
      </Box>
      <Box sx={{ '& p': { mt: 0, mb: 1, color: 'text.secondary', lineHeight: 1.6 }, '& ul': { pl: 3, m: 0, color: 'text.secondary' } }}>
        <ReactMarkdown>{content || "Not available."}</ReactMarkdown>
      </Box>
    </CardContent>
  </Card>
);

const InsightsPanel = ({ summary, gaps, future }) => {
  return (
    <Box>
      <InsightSection 
        title="Key Research Insights" 
        content={summary} 
        icon={<LightbulbIcon />} 
        color="#4285F4" 
      />
      <InsightSection 
        title="Research Gaps" 
        content={gaps} 
        icon={<WarningAmberIcon />} 
        color="#FBBC05" 
      />
      <InsightSection 
        title="Future Opportunities" 
        content={future} 
        icon={<ExploreIcon />} 
        color="#34A853" 
      />
    </Box>
  );
};

export default InsightsPanel;
