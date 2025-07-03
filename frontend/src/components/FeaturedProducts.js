import React from 'react';
import { useFeaturedProducts } from '../hooks/useProducts';
import ProductCard from './ProductCard';
import { LoadingGrid } from './LoadingSpinner';

const FeaturedProducts = () => {
  const { featuredProducts, loading, error } = useFeaturedProducts();

  if (loading) {
    return (
      <section id="featured" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-5xl font-bold text-gray-800 mb-4">
              Featured
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Products</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Handpicked selections from our best-selling items across all categories
            </p>
          </div>
          <LoadingGrid count={4} />
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="featured" className="py-20 px-4 bg-white">
        <div className="container mx-auto">
          <div className="text-center">
            <h2 className="text-5xl font-bold text-gray-800 mb-4">
              Featured
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Products</span>
            </h2>
            <p className="text-xl text-red-600">Error loading featured products: {error}</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section id="featured" className="py-20 px-4 bg-white">
      <div className="container mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-800 mb-4">
            Featured
            <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent"> Products</span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Handpicked selections from our best-selling items across all categories
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {featuredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturedProducts;