from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Схема заполнения создание товара
class ProductApp(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float = Field(ge=0.0)


# Схема для частичного обновления (все поля необязательные)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


# Схема для вывода
class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    price: float
    created_at: datetime


