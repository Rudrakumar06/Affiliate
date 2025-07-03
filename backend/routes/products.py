from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..models.product import Product, ProductCreate, ProductUpdate
from ..database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[Product])
async def get_products(
    category_id: Optional[str] = None,
    is_featured: Optional[bool] = None,
    limit: int = 50,
    skip: int = 0,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all products with optional filtering"""
    query = {"is_active": True}
    
    if category_id:
        query["category_id"] = category_id
    if is_featured is not None:
        query["is_featured"] = is_featured
    
    products = await db.products.find(query).skip(skip).limit(limit).to_list(limit)
    return [Product(**product) for product in products]

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a specific product by ID"""
    product = await db.products.find_one({"id": product_id, "is_active": True})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Create a new product"""
    # Check if category exists
    category = await db.categories.find_one({"id": product.category_id, "is_active": True})
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id")
    
    product_obj = Product(**product.dict())
    await db.products.insert_one(product_obj.dict())
    return product_obj

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: str, 
    product_update: ProductUpdate, 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a product"""
    # Check if product exists
    existing_product = await db.products.find_one({"id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # If category_id is being updated, verify it exists
    if product_update.category_id:
        category = await db.categories.find_one({"id": product_update.category_id, "is_active": True})
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category_id")
    
    # Update only provided fields
    update_data = {k: v for k, v in product_update.dict(exclude_unset=True).items()}
    
    await db.products.update_one(
        {"id": product_id}, 
        {"$set": update_data}
    )
    
    updated_product = await db.products.find_one({"id": product_id})
    return Product(**updated_product)

@router.delete("/{product_id}")
async def delete_product(product_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Soft delete a product"""
    result = await db.products.update_one(
        {"id": product_id}, 
        {"$set": {"is_active": False}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product deleted successfully"}

@router.get("/featured/list", response_model=List[Product])
async def get_featured_products(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get featured products"""
    products = await db.products.find({"is_featured": True, "is_active": True}).to_list(10)
    return [Product(**product) for product in products]