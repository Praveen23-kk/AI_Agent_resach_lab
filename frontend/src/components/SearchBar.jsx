import React from 'react';
import { Box, TextField, Button, CircularProgress } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

const SearchBar = ({ query, setQuery, onSearch, disabled }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(e);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', gap: 2, maxWidth: 800, mx: 'auto', width: '100%', mb: 4 }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="e.g., How does multi-agent reinforcement learning improve swarm robotics?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={disabled}
        sx={{
          '& .MuiOutlinedInput-root': {
            borderRadius: 24,
            backgroundColor: '#fff',
          }
        }}
      />
      <Button
        type="submit"
        variant="contained"
        color="primary"
        disabled={disabled || !query.trim()}
        startIcon={disabled ? <CircularProgress size={20} color="inherit" /> : <SearchIcon />}
        sx={{ borderRadius: 24, px: 4, flexShrink: 0 }}
      >
        {disabled ? 'Researching...' : 'Start Research'}
      </Button>
    </Box>
  );
};

export default SearchBar;
