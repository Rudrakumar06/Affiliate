from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.category import Category, CategoryCreate, CategoryUpdate, CategoryWithProducts
from ..database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[Category])
async def get_categories(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get all active categories"""
    categories = await db.categories.find({"is_active": True}).to_list(100)
    return [Category(**category) for category in categories]

@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a specific category by ID"""
    category = await db.categories.find_one({"id": category_id, "is_active": True})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category(**category)

@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(slug: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a category by slug"""
    category = await db.categories.find_one({"slug": slug, "is_active": True})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category(**category)

@router.get("/{category_id}/products", response_model=CategoryWithProducts)
async def get_category_with_products(category_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a category with its products"""
    # First get the category
    category = await db.categories.find_one({"id": category_id, "is_active": True})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Then get its products
    products = await db.products.find({"category_id": category_id, "is_active": True}).to_list(100)
    
    # Create response
    category_with_products = CategoryWithProducts(**category)
    category_with_products.products = products
    
    return category_with_products

@router.post("/", response_model=Category)
async def create_category(category: CategoryCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Create a new category"""
    # Check if slug already exists
    existing_category = await db.categories.find_one({"slug": category.slug})
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this slug already exists")
    
    category_obj = Category(**category.dict())
    await db.categories.insert_one(category_obj.dict())
    return category_obj

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: str, 
    category_update: CategoryUpdate, 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a category"""
    # Check if category exists
    existing_category = await db.categories.find_one({"id": category_id})
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # If slug is being updated, check for conflicts
    if category_update.slug:
        slug_conflict = await db.categories.find_one({
            "slug": category_update.slug, 
            "id": {"$ne": category_id}
        })
        if slug_conflict:
            raise HTTPException(status_code=400, detail="Category with this slug already exists")
    
    # Update only provided fields
    update_data = {k: v for k, v in category_update.dict(exclude_unset=True).items()}
    
    await db.categories.update_one(
        {"id": category_id}, 
        {"$set": update_data}
    )
    
    updated_category = await db.categories.find_one({"id": category_id})
    return Category(**updated_category)

@router.delete("/{category_id}")
async def delete_category(category_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Soft delete a category"""
    result = await db.categories.update_one(
        {"id": category_id}, 
        {"$set": {"is_active": False}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {"message": "Category deleted successfully"}