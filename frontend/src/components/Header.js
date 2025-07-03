import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/button';
import { Menu, X, Search, ShoppingCart, Heart } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="bg-white/95 backdrop-blur-sm sticky top-0 z-50 border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">AM</span>
            </div>
            <span className="text-xl font-bold text-gray-800">AffiliateMax</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Home
            </Link>
            <Link to="/category/cables" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Cables
            </Link>
            <Link to="/category/keyboards" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Keyboards
            </Link>
            <Link to="/category/mousepads" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Mouse Pads
            </Link>
            <Link to="/category/sound-absorbers" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Audio
            </Link>
            <Link to="/category/hair-care" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
              Hair Care
            </Link>
          </nav>

          {/* Right Side Icons */}
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon" className="hidden sm:flex">
              <Search className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="hidden sm:flex">
              <Heart className="h-5 w-5" />
            </Button>
            <Button variant="ghost" size="icon" className="hidden sm:flex">
              <ShoppingCart className="h-5 w-5" />
            </Button>
            
            {/* Mobile Menu Button */}
            <Button variant="ghost" size="icon" className="md:hidden" onClick={toggleMenu}>
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200 bg-white">
            <nav className="flex flex-col space-y-2">
              <Link to="/" className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Home
              </Link>
              <Link to="/category/cables" className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Cables
              </Link>
              <Link to="/category/keyboards" className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Keyboards
              </Link>
              <Link to="/category/mousepads" className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Mouse Pads
              </Link>
              <Link to="/category/sound-absorbers" className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Audio
              </Link>
              <Link to="/category/hair-care" className="block py-2 text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Hair Care
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;