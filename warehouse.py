from _datetime import datetime
from enum import Enum
from random import random

from pydantic import BaseModel, Field

from product import products_list, Product
from er import MyError

class MoveType(Enum):
    IN = 1
    OUT = 2

class StockResponse(BaseModel):
    product_id: int
    qty: int


class MovementApp(BaseModel):
    product_id: int
    type: MoveType
    qty: int = Field(0, ge=0)
    comment: str = ""

class Movement:
    def __init__(self, product_id:int, qty:int, type: MoveType):
        print(products_list)
        self.pid =  1
        self.product = Product.get_product_by_id(product_id)
        self.type = type
        self.qty = qty
        self.comment: str = ""
        self.created_at: datetime = datetime.now()

class Warehouse():

    def __init__(self,  wid: int):
        self.wid = wid
        # product_id: int
        # type: str  # осталось лишь IN and OUT
        # qty: int = Field(0, ge=0) # > 0
        # comment: str = ""
        self.created_at: datetime = Field(default_factory=datetime.now)
        self.movements = []


    @staticmethod
    def general_check(product_id: int):
        if product_id not in warehouse_dict:
            raise MyError(code=404, message="Товара нет")


    def add_move(self, move: Movement):

        if move.qty < 0:
            raise MyError(code=20, message="Движение не может быть отрицательным")

        qty_now = self.product_qty(move.product.pid)
        if qty_now<move.qty and move.type==MoveType.OUT:
            raise MyError(10, f"Недостаточно товара на складе. Количество {qty_now}")
        self.movements.append(move)

    def product_qty(self, product_id:int):

        product = Product.get_product_by_id(product_id)
        qty = 0
        for move in self.movements:
            if move.product == product:
                if move.type == MoveType.IN:
                    qty = qty + move.qty
                else:
                    qty = qty - move.qty

        return qty
    @classmethod
    def add_movement(cls, move: MovementApp):

        cls.general_check(product_id=move.product_id)

        if move.type == 'OUT' and warehouse_dict[move.product_id] < move.qty:
            raise MyError(code=400, message=f"Остатка на складе {warehouse_dict[move.product_id]}, поэтому не хватает")

        stock = cls(
            wid=len(history) + 1,
            product_id=move.product_id,
            type=move.type,
            qty=move.qty,
            comment=move.comment
        )
        history.append(stock)

        if move.type == 'OUT':
            warehouse_dict[move.product_id] -= move.qty
        else:
            warehouse_dict[move.product_id] += move.qty

        return stock

    @classmethod
    def remainder_product(cls, product_id: int):
        cls.general_check(product_id=product_id)

        return warehouse_dict[product_id]


warehouse_dict = {dict(key)['pid']: 0 for _, key in enumerate(products_list)}
history = []

p_wh = Warehouse(1)

p_wh.add_move(Movement(1, 100, MoveType.IN))
p_wh.add_move(Movement(1, 50, MoveType.OUT))

print(p_wh.product_qty(1))

print("--", p_wh.movements)

# print(vars(p_wh))

# print(products_list)

# print(warehouse_dict)
#
#
# print(Warehouse.add_movement(move=MovementApp(type="IN", qty=5)))
# print(Warehouse.add_movement(move=MovementApp(type="OUT", qty=3)))
# print(Warehouse.add_movement(move=MovementApp(type="IN", qty=8)))
# print(history)
#
# print(warehouse_dict)
#
# print(Warehouse.remainder_product(1))
