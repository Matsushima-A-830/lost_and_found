# Pydantic スキーマ
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class ErrorResponse(BaseModel):
    message: str

class ItemBase(BaseModel):
    found_datetime: datetime.datetime
    found_place: str
    category_l: str
    category_m: Optional[str] = None
    category_s: Optional[str] = None
    color: Optional[str] = None
    features: Optional[str] = None
    status: str
    image_path: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    management_number: str
    registered_by_user_id: Optional[int] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
