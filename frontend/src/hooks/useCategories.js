import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useCategories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await apiService.getCategories();
        setCategories(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching categories:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  return { categories, loading, error };
};

export const useCategory = (categoryId) => {
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategory = async () => {
      if (!categoryId) return;

      try {
        setLoading(true);
        setError(null);
        const data = await apiService.getCategory(categoryId);
        setCategory(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching category:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategory();
  }, [categoryId]);

  return { category, loading, error };
};

export const useCategoryBySlug = (slug) => {
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategory = async () => {
      if (!slug) return;

      try {
        setLoading(true);
        setError(null);
        const data = await apiService.getCategoryBySlug(slug);
        setCategory(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching category by slug:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategory();
  }, [slug]);

  return { category, loading, error };
};

export const useCategoryWithProducts = (categoryId) => {
  const [categoryWithProducts, setCategoryWithProducts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategoryWithProducts = async () => {
      if (!categoryId) return;

      try {
        setLoading(true);
        setError(null);
        const data = await apiService.getCategoryWithProducts(categoryId);
        setCategoryWithProducts(data);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching category with products:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategoryWithProducts();
  }, [categoryId]);

  return { categoryWithProducts, loading, error };
};