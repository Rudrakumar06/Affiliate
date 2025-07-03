import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Star, ShoppingCart, Heart } from 'lucide-react';

const ProductCard = ({ product }) => {
  const handleBuyNow = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
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

  const handleAddToWishlist = (e) => {
    e.preventDefault();
    e.stopPropagation();
    // Mock wishlist functionality
    alert(`${product.name} added to wishlist!`);
  };

  const discount = Math.round(((product.original_price - product.price) / product.original_price) * 100);

  return (
    <div className="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden">
      {/* Discount Badge */}
      {discount > 0 && (
        <div className="absolute top-4 left-4 z-10">
          <Badge variant="destructive" className="text-sm font-semibold">
            -{discount}% OFF
          </Badge>
        </div>
      )}

      {/* Wishlist Button */}
      <button 
        onClick={handleAddToWishlist}
        className="absolute top-4 right-4 z-10 w-10 h-10 bg-white/90 hover:bg-white rounded-full flex items-center justify-center shadow-md hover:shadow-lg transition-all duration-200 group-hover:scale-110"
      >
        <Heart className="h-5 w-5 text-gray-600 hover:text-red-500 transition-colors" />
      </button>

      <Link to={`/product/${product.id}`} className="block">
        {/* Product Image */}
        <div className="relative overflow-hidden">
          <img 
            src={product.image} 
            alt={product.name}
            className="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-300"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        {/* Product Info */}
        <div className="p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-blue-600 transition-colors">
            {product.name}
          </h3>
          
          <p className="text-gray-600 mb-3 text-sm leading-relaxed">
            {product.description}
          </p>

          {/* Rating */}
          <div className="flex items-center space-x-2 mb-4">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <Star 
                  key={i} 
                  className={`h-4 w-4 ${i < Math.floor(product.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                />
              ))}
            </div>
            <span className="text-sm font-medium text-gray-700">{product.rating}</span>
            <span className="text-sm text-gray-500">({product.reviews})</span>
          </div>

          {/* Price */}
          <div className="flex items-center space-x-2 mb-4">
            <span className="text-2xl font-bold text-green-600">${product.price}</span>
            {product.originalPrice > product.price && (
              <span className="text-sm text-gray-500 line-through">${product.originalPrice}</span>
            )}
          </div>

          {/* Features */}
          <div className="mb-4">
            <div className="flex flex-wrap gap-1">
              {product.features.slice(0, 2).map((feature, index) => (
                <span key={index} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-md">
                  {feature}
                </span>
              ))}
              {product.features.length > 2 && (
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-md">
                  +{product.features.length - 2} more
                </span>
              )}
            </div>
          </div>
        </div>
      </Link>

      {/* Buy Now Button */}
      <div className="px-6 pb-6">
        <Button 
          onClick={handleBuyNow}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 px-4 rounded-xl transform hover:scale-105 transition-all duration-200 shadow-md hover:shadow-lg"
        >
          <ShoppingCart className="h-4 w-4 mr-2" />
          Buy Now - ${product.price}
        </Button>
      </div>
    </div>
  );
};

export default ProductCard;