from typing import Optional

from pydantic import BaseModel, Field


# Схема заполнения создание товара
class ProductApp(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float = Field(0.0, ge=0.0)


# Схема для частичного обновления (все поля необязательные)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
