from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MoveType(Enum):
    IN = "IN"
    OUT = "OUT"


# Схема для добавления движения
class MovementApp(BaseModel):
    product_id: int = 1
    type: MoveType
    qty: int = Field(0, ge=0)
    comment: Optional[str] = None


# Схема вывода текущий остаток товара
class StockResponse(BaseModel):
    product_id: int
    qty: int
