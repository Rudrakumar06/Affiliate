from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    price: float
    original_price: float
    rating: float = Field(ge=0, le=5)
    reviews: int = Field(ge=0)
    image: str
    description: str
    features: List[str]
    affiliate_link: str
    category_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    is_featured: bool = False

class ProductCreate(BaseModel):
    name: str
    price: float
    original_price: float
    rating: float = Field(ge=0, le=5)
    reviews: int = Field(ge=0)
    image: str
    description: str
    features: List[str]
    affiliate_link: str
    category_id: str
    is_featured: bool = False

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    reviews: Optional[int] = Field(None, ge=0)
    image: Optional[str] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    affiliate_link: Optional[str] = None
    category_id: Optional[str] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)