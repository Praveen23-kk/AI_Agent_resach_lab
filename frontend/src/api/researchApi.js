import axios from 'axios';

// Connect to the FastAPI backend running locally
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const runResearch = async (query) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/research`, {
      query: query,
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      throw new Error(`Server Error: ${error.response.data.detail || error.response.statusText}`);
    } else if (error.request) {
      // The request was made but no response was received
      throw new Error("Cannot connect to server. Is FastAPI running on port 8000?");
    } else {
      // Something happened in setting up the request that triggered an Error
      throw new Error("Error initiating request: " + error.message);
    }
  }
};

export const comparePapers = async (paperA, paperB) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/compare`, {
      paperA: { title: paperA.title, abstract: paperA.abstract },
      paperB: { title: paperB.title, abstract: paperB.abstract }
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(`Comparison Failed: ${error.response.data.detail || error.response.statusText}`);
    } else {
      throw new Error("Failed to reach comparison endpoint.");
    }
  }
};

export const generateResearchIdeas = async (topic, context) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/research-ideas`, {
      topic: topic,
      context: context
    });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(`Idea Generator Failed: ${error.response.data.detail || error.response.statusText}`);
    } else {
      throw new Error("Failed to reach research-ideas endpoint.");
    }
  }
};
