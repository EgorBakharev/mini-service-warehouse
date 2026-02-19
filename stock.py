from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from product import Product
from er import MyError


class MoveType(Enum):
    IN = "IN"
    OUT = "OUT"


class StockResponse(BaseModel):
    product_id: int
    qty: int


class MovementApp(BaseModel):
    product_id: int = 1
    type: MoveType
    qty: int = Field(0, ge=0)
    comment: Optional[str] = None


class Movement:
    def __init__(self, product_id: int, qty: int, type: MoveType, comment: str = ''):
        self.pid: int
        self.product = Product.get_product_by_id(product_id)
        self.type = type
        self.qty = qty
        self.comment: str = comment
        self.created_at: datetime = datetime.now()


class Warehouse:
    # pid: int
    # product_id: Product
    # type: MoveType
    # qty: int = Field(0, ge=0)
    # comment: Optional[str] = None
    # created_at: datetime = Field(default_factory=datetime.now)
    # move_list: []
    def __init__(self, wid: int):
        self.wid = wid
        self.created_at: datetime = Field(default_factory=datetime.now)
        self.movements = []


    @staticmethod
    def get_product(product_id):
        return Product.get_product_by_id(product_id)

    def add_move(self, move: Movement):

        if move.qty <= 0:
            raise MyError(code=422, message="Движение не может быть отрицательным")

        qty_now = self.product_qty(move.product.pid)
        if qty_now < move.qty and move.type == MoveType.OUT:
            raise MyError(400, f"Недостаточно товара на складе. Количество {qty_now}")
        self.movements.append(move)

    def product_qty(self, product_id: int):
        product = Product.get_product_by_id(product_id)
        qty = 0
        for move in self.movements:
            if move.product == product:
                if move.type == MoveType.IN:
                    qty = qty + move.qty
                else:
                    qty = qty - move.qty

        return qty

    def stock_list(self):
        return self.movements