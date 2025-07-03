#!/usr/bin/env python3
import requests
import json
import sys
import os
from typing import Dict, List, Any, Optional

# Get the backend URL from the frontend .env file
def get_backend_url():
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                return line.strip().split('=')[1]
    return None

# Base URL for API requests
BASE_URL = f"{get_backend_url()}/api"
print(f"Using API base URL: {BASE_URL}")

# Test results tracking
test_results = {
    "passed": 0,
    "failed": 0,
    "tests": []
}

def log_test(name: str, passed: bool, response: Optional[requests.Response] = None, error: Optional[str] = None):
    """Log test results with details"""
    status = "✅ PASSED" if passed else "❌ FAILED"
    
    result = {
        "name": name,
        "passed": passed
    }
    
    if response:
        try:
            result["status_code"] = response.status_code
            result["response"] = response.json() if response.headers.get('content-type') == 'application/json' else str(response.text)[:100]
        except:
            result["response"] = "Could not parse response"
    
    if error:
        result["error"] = error
    
    test_results["tests"].append(result)
    
    if passed:
        test_results["passed"] += 1
    else:
        test_results["failed"] += 1
    
    print(f"{status} - {name}")
    if not passed and error:
        print(f"  Error: {error}")
    if response:
        print(f"  Status: {response.status_code}")
        try:
            if response.headers.get('content-type') == 'application/json':
                print(f"  Response: {json.dumps(response.json(), indent=2)[:200]}...")
            else:
                print(f"  Response: {response.text[:200]}...")
        except:
            print(f"  Response: Could not parse response")
    print()

def test_api_health():
    """Test the API health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        passed = response.status_code == 200 and response.json().get("status") == "healthy"
        log_test("API Health Check", passed, response)
        return passed
    except Exception as e:
        log_test("API Health Check", False, error=str(e))
        return False

def test_seed_status():
    """Test the seed status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/seed/status")
        passed = response.status_code == 200 and "is_seeded" in response.json()
        log_test("Seed Status Check", passed, response)
        return passed
    except Exception as e:
        log_test("Seed Status Check", False, error=str(e))
        return False

def test_seed_data():
    """Test the data seeding endpoint"""
    try:
        response = requests.post(f"{BASE_URL}/seed/initial-data")
        passed = response.status_code == 200 and "message" in response.json()
        log_test("Data Seeding", passed, response)
        return passed
    except Exception as e:
        log_test("Data Seeding", False, error=str(e))
        return False

def test_get_all_products():
    """Test getting all products"""
    try:
        response = requests.get(f"{BASE_URL}/products")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        log_test("Get All Products", passed, response)
        return passed, response.json() if passed else []
    except Exception as e:
        log_test("Get All Products", False, error=str(e))
        return False, []

def test_get_featured_products():
    """Test getting featured products"""
    try:
        response = requests.get(f"{BASE_URL}/products/featured/list")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        # Verify all returned products have is_featured=True
        if passed and response.json():
            all_featured = all(product.get("is_featured", False) for product in response.json())
            passed = passed and all_featured
        log_test("Get Featured Products", passed, response)
        return passed
    except Exception as e:
        log_test("Get Featured Products", False, error=str(e))
        return False

def test_filter_products_by_category(category_id: str):
    """Test filtering products by category"""
    try:
        response = requests.get(f"{BASE_URL}/products", params={"category_id": category_id})
        passed = response.status_code == 200 and isinstance(response.json(), list)
        # Verify all returned products have the correct category_id
        if passed and response.json():
            all_match_category = all(product.get("category_id") == category_id for product in response.json())
            passed = passed and all_match_category
        log_test(f"Filter Products by Category (ID: {category_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Filter Products by Category (ID: {category_id})", False, error=str(e))
        return False

def test_get_product_by_id(product_id: str):
    """Test getting a product by ID"""
    try:
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        passed = response.status_code == 200 and response.json().get("id") == product_id
        log_test(f"Get Product by ID (ID: {product_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Get Product by ID (ID: {product_id})", False, error=str(e))
        return False

def test_get_all_categories():
    """Test getting all categories"""
    try:
        response = requests.get(f"{BASE_URL}/categories")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        log_test("Get All Categories", passed, response)
        return passed, response.json() if passed else []
    except Exception as e:
        log_test("Get All Categories", False, error=str(e))
        return False, []

def test_get_category_by_id(category_id: str):
    """Test getting a category by ID"""
    try:
        response = requests.get(f"{BASE_URL}/categories/{category_id}")
        passed = response.status_code == 200 and response.json().get("id") == category_id
        log_test(f"Get Category by ID (ID: {category_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Get Category by ID (ID: {category_id})", False, error=str(e))
        return False

def test_get_category_by_slug(slug: str):
    """Test getting a category by slug"""
    try:
        response = requests.get(f"{BASE_URL}/categories/slug/{slug}")
        passed = response.status_code == 200 and response.json().get("slug") == slug
        log_test(f"Get Category by Slug (Slug: {slug})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Get Category by Slug (Slug: {slug})", False, error=str(e))
        return False

def test_get_category_with_products(category_id: str):
    """Test getting a category with its products"""
    try:
        response = requests.get(f"{BASE_URL}/categories/{category_id}/products")
        passed = (
            response.status_code == 200 and 
            response.json().get("id") == category_id and
            "products" in response.json()
        )
        # Verify all products have the correct category_id
        if passed and response.json().get("products"):
            all_match_category = all(
                product.get("category_id") == category_id 
                for product in response.json().get("products", [])
            )
            passed = passed and all_match_category
        log_test(f"Get Category with Products (ID: {category_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Get Category with Products (ID: {category_id})", False, error=str(e))
        return False

def test_get_all_testimonials():
    """Test getting all testimonials"""
    try:
        response = requests.get(f"{BASE_URL}/testimonials")
        passed = response.status_code == 200 and isinstance(response.json(), list)
        log_test("Get All Testimonials", passed, response)
        return passed
    except Exception as e:
        log_test("Get All Testimonials", False, error=str(e))
        return False

def test_create_product():
    """Test creating a new product"""
    # First get a valid category ID
    success, categories = test_get_all_categories()
    if not success or not categories:
        log_test("Create Product", False, error="Could not get categories to create product")
        return False
    
    category_id = categories[0]["id"]
    
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "original_price": 129.99,
        "rating": 4.5,
        "reviews": 42,
        "image": "https://example.com/test-image.jpg",
        "description": "This is a test product created by the test script",
        "features": ["Feature 1", "Feature 2", "Feature 3"],
        "affiliate_link": "https://example.com/affiliate/test-product",
        "category_id": category_id,
        "is_featured": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products", json=product_data)
        passed = (
            response.status_code == 200 and
            response.json().get("name") == product_data["name"] and
            response.json().get("category_id") == category_id
        )
        log_test("Create Product", passed, response)
        return passed, response.json().get("id") if passed else None
    except Exception as e:
        log_test("Create Product", False, error=str(e))
        return False, None

def test_update_product(product_id: str):
    """Test updating a product"""
    update_data = {
        "name": "Updated Test Product",
        "price": 89.99,
        "description": "This product was updated by the test script"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
        passed = (
            response.status_code == 200 and
            response.json().get("id") == product_id and
            response.json().get("name") == update_data["name"] and
            response.json().get("price") == update_data["price"]
        )
        log_test(f"Update Product (ID: {product_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Update Product (ID: {product_id})", False, error=str(e))
        return False

def test_delete_product(product_id: str):
    """Test deleting a product (soft delete)"""
    try:
        response = requests.delete(f"{BASE_URL}/products/{product_id}")
        passed = response.status_code == 200 and "message" in response.json()
        
        # Verify the product is now marked as inactive
        if passed:
            get_response = requests.get(f"{BASE_URL}/products/{product_id}")
            # Should return 404 since soft-deleted products are filtered out
            passed = get_response.status_code == 404
        
        log_test(f"Delete Product (ID: {product_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Delete Product (ID: {product_id})", False, error=str(e))
        return False

def test_create_category():
    """Test creating a new category"""
    category_data = {
        "name": "Test Category",
        "description": "This is a test category created by the test script",
        "icon": "🧪",
        "slug": "test-category"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/categories", json=category_data)
        passed = (
            response.status_code == 200 and
            response.json().get("name") == category_data["name"] and
            response.json().get("slug") == category_data["slug"]
        )
        log_test("Create Category", passed, response)
        return passed, response.json().get("id") if passed else None
    except Exception as e:
        log_test("Create Category", False, error=str(e))
        return False, None

def test_update_category(category_id: str):
    """Test updating a category"""
    update_data = {
        "name": "Updated Test Category",
        "description": "This category was updated by the test script"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/categories/{category_id}", json=update_data)
        passed = (
            response.status_code == 200 and
            response.json().get("id") == category_id and
            response.json().get("name") == update_data["name"]
        )
        log_test(f"Update Category (ID: {category_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Update Category (ID: {category_id})", False, error=str(e))
        return False

def test_delete_category(category_id: str):
    """Test deleting a category (soft delete)"""
    try:
        response = requests.delete(f"{BASE_URL}/categories/{category_id}")
        passed = response.status_code == 200 and "message" in response.json()
        
        # Verify the category is now marked as inactive
        if passed:
            get_response = requests.get(f"{BASE_URL}/categories/{category_id}")
            # Should return 404 since soft-deleted categories are filtered out
            passed = get_response.status_code == 404
        
        log_test(f"Delete Category (ID: {category_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Delete Category (ID: {category_id})", False, error=str(e))
        return False

def test_create_testimonial():
    """Test creating a new testimonial"""
    testimonial_data = {
        "name": "Test User",
        "role": "QA Tester",
        "content": "This is a test testimonial created by the test script",
        "rating": 5,
        "image": "https://example.com/test-user.jpg"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/testimonials", json=testimonial_data)
        passed = (
            response.status_code == 200 and
            response.json().get("name") == testimonial_data["name"] and
            response.json().get("rating") == testimonial_data["rating"]
        )
        log_test("Create Testimonial", passed, response)
        return passed, response.json().get("id") if passed else None
    except Exception as e:
        log_test("Create Testimonial", False, error=str(e))
        return False, None

def test_update_testimonial(testimonial_id: str):
    """Test updating a testimonial"""
    update_data = {
        "name": "Updated Test User",
        "content": "This testimonial was updated by the test script"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/testimonials/{testimonial_id}", json=update_data)
        passed = (
            response.status_code == 200 and
            response.json().get("id") == testimonial_id and
            response.json().get("name") == update_data["name"]
        )
        log_test(f"Update Testimonial (ID: {testimonial_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Update Testimonial (ID: {testimonial_id})", False, error=str(e))
        return False

def test_delete_testimonial(testimonial_id: str):
    """Test deleting a testimonial (soft delete)"""
    try:
        response = requests.delete(f"{BASE_URL}/testimonials/{testimonial_id}")
        passed = response.status_code == 200 and "message" in response.json()
        
        # Verify the testimonial is now marked as inactive
        if passed:
            get_response = requests.get(f"{BASE_URL}/testimonials/{testimonial_id}")
            # Should return 404 since soft-deleted testimonials are filtered out
            passed = get_response.status_code == 404
        
        log_test(f"Delete Testimonial (ID: {testimonial_id})", passed, response)
        return passed
    except Exception as e:
        log_test(f"Delete Testimonial (ID: {testimonial_id})", False, error=str(e))
        return False

def run_all_tests():
    """Run all API tests"""
    print("🧪 Starting API Tests for Affiliate Marketing Backend\n")
    
    # Basic health and seed checks
    test_api_health()
    test_seed_status()
    
    # Seed data if needed
    seed_success = test_seed_data()
    
    # Test product endpoints
    success, products = test_get_all_products()
    if success and products:
        product_id = products[0]["id"]
        category_id = products[0]["category_id"]
        
        test_get_featured_products()
        test_filter_products_by_category(category_id)
        test_get_product_by_id(product_id)
    
    # Test category endpoints
    success, categories = test_get_all_categories()
    if success and categories:
        category_id = categories[0]["id"]
        slug = categories[0]["slug"]
        
        test_get_category_by_id(category_id)
        test_get_category_by_slug(slug)
        test_get_category_with_products(category_id)
    
    # Test testimonial endpoints
    test_get_all_testimonials()
    
    # Test CRUD operations
    success, new_product_id = test_create_product()
    if success and new_product_id:
        test_update_product(new_product_id)
        test_delete_product(new_product_id)
    
    success, new_category_id = test_create_category()
    if success and new_category_id:
        test_update_category(new_category_id)
        test_delete_category(new_category_id)
    
    success, new_testimonial_id = test_create_testimonial()
    if success and new_testimonial_id:
        test_update_testimonial(new_testimonial_id)
        test_delete_testimonial(new_testimonial_id)
    
    # Print summary
    print("\n🧪 Test Summary:")
    print(f"Total Tests: {test_results['passed'] + test_results['failed']}")
    print(f"Passed: {test_results['passed']}")
    print(f"Failed: {test_results['failed']}")
    
    return test_results["failed"] == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)