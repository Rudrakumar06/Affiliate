from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.testimonial import Testimonial, TestimonialCreate, TestimonialUpdate
from ..database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/testimonials", tags=["testimonials"])

@router.get("/", response_model=List[Testimonial])
async def get_testimonials(
    limit: int = 10,
    skip: int = 0,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all active testimonials"""
    testimonials = await db.testimonials.find({"is_active": True}).skip(skip).limit(limit).to_list(limit)
    return [Testimonial(**testimonial) for testimonial in testimonials]

@router.get("/{testimonial_id}", response_model=Testimonial)
async def get_testimonial(testimonial_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Get a specific testimonial by ID"""
    testimonial = await db.testimonials.find_one({"id": testimonial_id, "is_active": True})
    if not testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return Testimonial(**testimonial)

@router.post("/", response_model=Testimonial)
async def create_testimonial(testimonial: TestimonialCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Create a new testimonial"""
    testimonial_obj = Testimonial(**testimonial.dict())
    await db.testimonials.insert_one(testimonial_obj.dict())
    return testimonial_obj

@router.put("/{testimonial_id}", response_model=Testimonial)
async def update_testimonial(
    testimonial_id: str, 
    testimonial_update: TestimonialUpdate, 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update a testimonial"""
    # Check if testimonial exists
    existing_testimonial = await db.testimonials.find_one({"id": testimonial_id})
    if not existing_testimonial:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    # Update only provided fields
    update_data = {k: v for k, v in testimonial_update.dict(exclude_unset=True).items()}
    
    await db.testimonials.update_one(
        {"id": testimonial_id}, 
        {"$set": update_data}
    )
    
    updated_testimonial = await db.testimonials.find_one({"id": testimonial_id})
    return Testimonial(**updated_testimonial)

@router.delete("/{testimonial_id}")
async def delete_testimonial(testimonial_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Soft delete a testimonial"""
    result = await db.testimonials.update_one(
        {"id": testimonial_id}, 
        {"$set": {"is_active": False}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    return {"message": "Testimonial deleted successfully"}