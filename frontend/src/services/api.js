import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API Service Functions
export const apiService = {
  // Products
  async getProducts(params = {}) {
    const response = await api.get('/products', { params });
    return response.data;
  },

  async getProduct(productId) {
    const response = await api.get(`/products/${productId}`);
    return response.data;
  },

  async getFeaturedProducts() {
    const response = await api.get('/products/featured/list');
    return response.data;
  },

  // Categories
  async getCategories() {
    const response = await api.get('/categories');
    return response.data;
  },

  async getCategory(categoryId) {
    const response = await api.get(`/categories/${categoryId}`);
    return response.data;
  },

  async getCategoryBySlug(slug) {
    const response = await api.get(`/categories/slug/${slug}`);
    return response.data;
  },

  async getCategoryWithProducts(categoryId) {
    const response = await api.get(`/categories/${categoryId}/products`);
    return response.data;
  },

  // Testimonials
  async getTestimonials(params = {}) {
    const response = await api.get('/testimonials', { params });
    return response.data;
  },

  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },

  // Seed data (for development)
  async seedInitialData() {
    const response = await api.post('/seed/initial-data');
    return response.data;
  },

  async getSeedStatus() {
    const response = await api.get('/seed/status');
    return response.data;
  }
};

export default apiService;