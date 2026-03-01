from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# Ограничение ввода
class MoveType(Enum):
    IN = "IN"
    OUT = "OUT"


# Схема для добавления движения
class MovementApp(BaseModel):
    product_id: int
    warehouse_id: int
    type: MoveType
    qty: int = Field(ge=1)
    comment: Optional[str] = None


# Схема вывода текущий остаток товара
class StockResponse(BaseModel):
    product_id: int
    qty: int


# Схема полного вывода
class MovementResponse(BaseModel):
    ...
