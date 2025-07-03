import React from 'react';
import { useParams } from 'react-router-dom';
import { useCategoryBySlug } from '../hooks/useCategories';
import { useProducts } from '../hooks/useProducts';
import Header from '../components/Header';
import ProductCard from '../components/ProductCard';
import Footer from '../components/Footer';
import LoadingSpinner, { LoadingGrid } from '../components/LoadingSpinner';

const ProductCategory = () => {
  const { categoryId } = useParams();
  const { category, loading: categoryLoading, error: categoryError } = useCategoryBySlug(categoryId);
  const { products, loading: productsLoading, error: productsError } = useProducts(
    category ? { category_id: category.id } : {}
  );

  const loading = categoryLoading || productsLoading;
  const error = categoryError || productsError;

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Header />
        <div className="container mx-auto px-4 py-20">
          <LoadingSpinner size="lg" className="mb-16" />
          <LoadingGrid count={6} />
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !category) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Header />
        <div className="container mx-auto px-4 py-20 text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Category Not Found</h1>
          <p className="text-lg text-gray-600">
            {error ? `Error: ${error}` : "The category you're looking for doesn't exist."}
          </p>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Header />
      <div className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <div className="text-6xl mb-4">{category.icon}</div>
          <h1 className="text-5xl font-bold text-gray-800 mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            {category.name}
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            {category.description}
          </p>
        </div>
        
        {products.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <p className="text-xl text-gray-600">No products found in this category.</p>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default ProductCategory;