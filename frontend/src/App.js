import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ProductCategory from './pages/ProductCategory';
import ProductDetail from './pages/ProductDetail';
import { Toaster } from './components/ui/toaster';
import './App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/category/:categoryId" element={<ProductCategory />} />
          <Route path="/product/:productId" element={<ProductDetail />} />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;