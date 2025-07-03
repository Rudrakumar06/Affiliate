import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useTestimonials = (params = {}) => {
  const [testimonials, setTestimonials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTestimonials = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await apiService.getTestimonials(params);
        setTestimonials(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching testimonials:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTestimonials();
  }, [JSON.stringify(params)]);

  return { testimonials, loading, error };
};