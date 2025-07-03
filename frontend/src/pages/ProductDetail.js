import React from 'react';
import { useParams } from 'react-router-dom';
import { useProduct } from '../hooks/useProducts';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Star, ShoppingCart, Heart, Share2 } from 'lucide-react';
import LoadingSpinner from '../components/LoadingSpinner';

const ProductDetail = () => {
  const { productId } = useParams();
  const { product, loading, error } = useProduct(productId);

  const handleBuyNow = () => {
    if (product?.affiliate_link) {
      // Check if it's a placeholder link
      if (product.affiliate_link.startsWith('PLACEHOLDER_')) {
        alert(`Affiliate link not yet configured: ${product.affiliate_link}`);
      } else {
        // Redirect to actual affiliate link
        window.open(product.affiliate_link, '_blank');
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Header />
        <div className="container mx-auto px-4 py-20">
          <LoadingSpinner size="xl" />
        </div>
        <Footer />
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        <Header />
        <div className="container mx-auto px-4 py-20 text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Product Not Found</h1>
          <p className="text-lg text-gray-600">
            {error ? `Error: ${error}` : "The product you're looking for doesn't exist."}
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
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
          {/* Product Image */}
          <div className="relative">
            <img 
              src={product.image} 
              alt={product.name}
              className="w-full h-96 object-cover rounded-2xl shadow-2xl transform hover:scale-105 transition-transform duration-300"
            />
            <div className="absolute top-4 right-4 flex space-x-2">
              <Button size="icon" variant="outline" className="bg-white/90 hover:bg-white">
                <Heart className="h-5 w-5" />
              </Button>
              <Button size="icon" variant="outline" className="bg-white/90 hover:bg-white">
                <Share2 className="h-5 w-5" />
              </Button>
            </div>
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-bold text-gray-800 mb-2">{product.name}</h1>
              <div className="flex items-center space-x-2 mb-4">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <Star 
                      key={i} 
                      className={`h-5 w-5 ${i < Math.floor(product.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                    />
                  ))}
                </div>
                <span className="text-lg font-semibold text-gray-700">{product.rating}</span>
                <span className="text-gray-500">({product.reviews} reviews)</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <span className="text-3xl font-bold text-green-600">${product.price}</span>
              <span className="text-xl text-gray-500 line-through">${product.original_price}</span>
              <Badge variant="destructive" className="text-sm">
                Save ${(product.original_price - product.price).toFixed(2)}
              </Badge>
            </div>

            <p className="text-lg text-gray-600 leading-relaxed">{product.description}</p>

            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Key Features</h3>
              <ul className="space-y-2">
                {product.features.map((feature, index) => (
                  <li key={index} className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex space-x-4">
              <Button 
                size="lg" 
                className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 px-8 rounded-xl transform hover:scale-105 transition-all duration-200"
                onClick={handleBuyNow}
              >
                <ShoppingCart className="h-5 w-5 mr-2" />
                Buy Now - ${product.price}
              </Button>
              <Button 
                size="lg" 
                variant="outline" 
                className="border-2 border-blue-600 text-blue-600 hover:bg-blue-50 font-semibold py-3 px-8 rounded-xl"
              >
                Add to Wishlist
              </Button>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ProductDetail;