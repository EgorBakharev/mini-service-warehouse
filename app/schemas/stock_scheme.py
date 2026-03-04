from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Ограничение ввода
class MoveType(Enum):
    IN = "IN"
    OUT = "OUT"


# Схема для добавления движения
class MovementApp(BaseModel):
    product_id: int
    warehouse_id: int
    type: MoveType
    qty: int = 0
    comment: Optional[str] = None


# Схема вывода текущий остаток товара
class StockResponse(BaseModel):
    product_id: int
    qty: int


# Схема полного вывода
class MovementResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    type: MoveType
    qty: int
    comment: Optional[str]
    created_at: datetime
