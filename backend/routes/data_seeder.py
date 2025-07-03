from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.product import Product
from ..models.category import Category
from ..models.testimonial import Testimonial

router = APIRouter(prefix="/seed", tags=["data-seeder"])

@router.post("/initial-data")
async def seed_initial_data(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Seed the database with initial data"""
    
    # Clear existing data
    await db.categories.delete_many({})
    await db.products.delete_many({})
    await db.testimonials.delete_many({})
    
    # Create categories
    categories_data = [
        {
            "name": "Cables & Accessories",
            "description": "High-quality cables for all your connectivity needs",
            "icon": "🔌",
            "slug": "cables"
        },
        {
            "name": "OTG Adapters",
            "description": "Connect your devices seamlessly with OTG technology",
            "icon": "🔄",
            "slug": "otg"
        },
        {
            "name": "Keyboards",
            "description": "Professional keyboards for productivity and gaming",
            "icon": "⌨️",
            "slug": "keyboards"
        },
        {
            "name": "Mouse Pads",
            "description": "Precision mouse pads for enhanced control and comfort",
            "icon": "🖱️",
            "slug": "mousepads"
        },
        {
            "name": "Sound Absorbers",
            "description": "Acoustic panels for better sound quality and noise reduction",
            "icon": "🔊",
            "slug": "sound-absorbers"
        },
        {
            "name": "Hair Care",
            "description": "Premium shampoo and conditioner for healthy hair",
            "icon": "💇",
            "slug": "hair-care"
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category = Category(**cat_data)
        categories.append(category)
        await db.categories.insert_one(category.dict())
    
    # Create products
    products_data = [
        # Cables
        {
            "name": "Premium USB-C Cable",
            "price": 29.99,
            "original_price": 39.99,
            "rating": 4.8,
            "reviews": 256,
            "image": "https://images.unsplash.com/photo-1558618900-fcd25c85cd64?w=400&h=300&fit=crop",
            "description": "Fast charging and data transfer with durable braided design",
            "features": ["Fast Charging", "480Mbps Data Transfer", "Durable Braided Design", "6ft Length"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_1",
            "category_id": categories[0].id,
            "is_featured": True
        },
        {
            "name": "4K HDMI Cable",
            "price": 19.99,
            "original_price": 29.99,
            "rating": 4.7,
            "reviews": 189,
            "image": "https://images.unsplash.com/photo-1558618900-fcd25c85cd64?w=400&h=300&fit=crop",
            "description": "Ultra-high-speed HDMI cable supporting 4K@60Hz",
            "features": ["4K@60Hz Support", "Gold-Plated Connectors", "Ethernet Channel", "10ft Length"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_2",
            "category_id": categories[0].id
        },
        # OTG
        {
            "name": "USB-C OTG Adapter",
            "price": 12.99,
            "original_price": 18.99,
            "rating": 4.6,
            "reviews": 342,
            "image": "https://images.unsplash.com/photo-1558618900-fcd25c85cd64?w=400&h=300&fit=crop",
            "description": "Connect USB devices to your USB-C smartphone or tablet",
            "features": ["USB-C to USB-A", "Plug & Play", "Compact Design", "Fast Data Transfer"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_3",
            "category_id": categories[1].id
        },
        {
            "name": "Micro USB OTG Cable",
            "price": 9.99,
            "original_price": 14.99,
            "rating": 4.5,
            "reviews": 278,
            "image": "https://images.unsplash.com/photo-1558618900-fcd25c85cd64?w=400&h=300&fit=crop",
            "description": "Universal OTG cable for micro USB devices",
            "features": ["Micro USB to USB-A", "Universal Compatibility", "Durable Build", "6 inch Length"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_4",
            "category_id": categories[1].id
        },
        # Keyboards
        {
            "name": "RGB Mechanical Keyboard",
            "price": 89.99,
            "original_price": 119.99,
            "rating": 4.9,
            "reviews": 156,
            "image": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400&h=300&fit=crop",
            "description": "Premium mechanical keyboard with RGB backlighting",
            "features": ["Blue Switches", "RGB Backlighting", "Anti-Ghosting", "Aluminum Frame"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_5",
            "category_id": categories[2].id,
            "is_featured": True
        },
        {
            "name": "Wireless Compact Keyboard",
            "price": 49.99,
            "original_price": 69.99,
            "rating": 4.6,
            "reviews": 234,
            "image": "https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400&h=300&fit=crop",
            "description": "Slim wireless keyboard perfect for work and travel",
            "features": ["Wireless Connectivity", "Compact Design", "Long Battery Life", "Quiet Keys"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_6",
            "category_id": categories[2].id
        },
        # Mouse Pads
        {
            "name": "Large Gaming Mouse Pad",
            "price": 24.99,
            "original_price": 34.99,
            "rating": 4.7,
            "reviews": 445,
            "image": "https://images.unsplash.com/photo-1538300342682-cf57afb97285?w=400&h=300&fit=crop",
            "description": "Extended gaming mouse pad with RGB lighting",
            "features": ["RGB Lighting", "Water Resistant", "Non-Slip Base", "35\" x 15\" Size"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_7",
            "category_id": categories[3].id,
            "is_featured": True
        },
        {
            "name": "Ergonomic Office Mouse Pad",
            "price": 16.99,
            "original_price": 24.99,
            "rating": 4.5,
            "reviews": 298,
            "image": "https://images.unsplash.com/photo-1538300342682-cf57afb97285?w=400&h=300&fit=crop",
            "description": "Ergonomic mouse pad with wrist support",
            "features": ["Wrist Support", "Memory Foam", "Smooth Surface", "Professional Design"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_8",
            "category_id": categories[3].id
        },
        # Sound Absorbers
        {
            "name": "Acoustic Foam Panels",
            "price": 39.99,
            "original_price": 59.99,
            "rating": 4.8,
            "reviews": 167,
            "image": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&h=300&fit=crop",
            "description": "Professional acoustic foam panels for sound treatment",
            "features": ["12-Pack", "Noise Reduction", "Easy Installation", "Fire Resistant"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_9",
            "category_id": categories[4].id
        },
        {
            "name": "Corner Bass Traps",
            "price": 79.99,
            "original_price": 99.99,
            "rating": 4.6,
            "reviews": 89,
            "image": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400&h=300&fit=crop",
            "description": "Professional bass traps for corner acoustic treatment",
            "features": ["Set of 4", "Bass Frequency Control", "Corner Design", "Professional Grade"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_10",
            "category_id": categories[4].id
        },
        # Hair Care
        {
            "name": "Organic Argan Oil Shampoo",
            "price": 24.99,
            "original_price": 34.99,
            "rating": 4.9,
            "reviews": 523,
            "image": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=300&fit=crop",
            "description": "Luxurious argan oil shampoo for all hair types",
            "features": ["Organic Ingredients", "Sulfate-Free", "Color Safe", "16 fl oz"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_11",
            "category_id": categories[5].id,
            "is_featured": True
        },
        {
            "name": "Keratin Repair Conditioner",
            "price": 26.99,
            "original_price": 36.99,
            "rating": 4.8,
            "reviews": 412,
            "image": "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=400&h=300&fit=crop",
            "description": "Deep conditioning treatment with keratin proteins",
            "features": ["Keratin Proteins", "Deep Repair", "Frizz Control", "16 fl oz"],
            "affiliate_link": "PLACEHOLDER_AFFILIATE_LINK_12",
            "category_id": categories[5].id
        }
    ]
    
    products = []
    for prod_data in products_data:
        product = Product(**prod_data)
        products.append(product)
        await db.products.insert_one(product.dict())
    
    # Create testimonials
    testimonials_data = [
        {
            "name": "Sarah Johnson",
            "role": "Tech Enthusiast",
            "content": "Amazing quality products! The USB-C cable I ordered works perfectly and charges my devices super fast.",
            "rating": 5,
            "image": "https://images.unsplash.com/photo-1494790108755-2616b5b7b813?w=100&h=100&fit=crop&crop=face"
        },
        {
            "name": "Mike Chen",
            "role": "Gamer",
            "content": "The mechanical keyboard is incredible! The RGB lighting and tactile feedback make gaming so much better.",
            "rating": 5,
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face"
        },
        {
            "name": "Emily Rodriguez",
            "role": "Content Creator",
            "content": "The acoustic panels transformed my home studio. Crystal clear audio recording now!",
            "rating": 5,
            "image": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop&crop=face"
        }
    ]
    
    testimonials = []
    for test_data in testimonials_data:
        testimonial = Testimonial(**test_data)
        testimonials.append(testimonial)
        await db.testimonials.insert_one(testimonial.dict())
    
    return {
        "message": "Initial data seeded successfully",
        "categories_created": len(categories),
        "products_created": len(products),
        "testimonials_created": len(testimonials)
    }

@router.get("/status")
async def get_seed_status(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Check the current status of seeded data"""
    categories_count = await db.categories.count_documents({})
    products_count = await db.products.count_documents({})
    testimonials_count = await db.testimonials.count_documents({})
    
    return {
        "categories": categories_count,
        "products": products_count,
        "testimonials": testimonials_count,
        "is_seeded": categories_count > 0 and products_count > 0 and testimonials_count > 0
    }