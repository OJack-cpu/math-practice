import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
});

export const getKnowledgePoints = (category) =>
  api.get('/knowledge-points', { params: { category } });

export const getQuestions = (params) =>
  api.get('/questions', { params });

export const getQuestion = (id) =>
  api.get(`/questions/${id}`);

export const submitAnswer = (data) =>
  api.post('/answer', data);

export const getDashboard = () =>
  api.get('/dashboard');

export const getDueReviews = (limit = 20) =>
  api.get('/review/due', { params: { limit } });

export const getErrorBook = (limit = 20) =>
  api.get('/error-book', { params: { limit } });

export const getWeakPoints = (minAttempts = 3) =>
  api.get('/analysis/weak-points', { params: { min_attempts: minAttempts } });

export const getCorrectRateTrend = (days = 14) =>
  api.get('/stats/correct-rate-trend', { params: { days } });

export default api;
