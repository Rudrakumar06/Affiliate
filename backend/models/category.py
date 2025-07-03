from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Category(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: str
    slug: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class CategoryCreate(BaseModel):
    name: str
    description: str
    icon: str
    slug: str

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class CategoryWithProducts(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    slug: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    products: List[dict] = []