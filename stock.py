from datetime import datetime

from er import MyError
from product import Product
from scheme_stock import MoveType


class Movement:
    def __init__(self, product_id: int, qty: int, type: MoveType, comment: str):
        self.pid = 0
        self.product = Product.get_product_by_id(product_id)
        self.type = type
        self.qty = qty
        self.comment: str = comment
        self.created_at: datetime = datetime.now()


class Warehouse:
    movements = []

    @staticmethod
    def get_product(product_id):
        return Product.get_product_by_id(product_id)

    @classmethod
    def add_move(cls, move: Movement):

        if move.qty <= 0:
            raise MyError(code=422, message="Движение не может быть отрицательным или нулевым")

        qty_now = cls.product_qty(move.product.pid)
        if qty_now < move.qty and move.type == MoveType.OUT:
            raise MyError(400, f"Недостаточно товара на складе. Количество {qty_now}")

        move.pid = len(cls.movements) + 1
        cls.movements.append(move)

    @classmethod
    def product_qty(cls, product_id: int):
        product = Product.get_product_by_id(product_id)

        qty = 0
        for move in cls.movements:
            if move.product == product:
                if move.type == MoveType.IN:
                    qty = qty + move.qty
                else:
                    qty = qty - move.qty

        return qty

    @classmethod
    def stock_movements(cls):
        return cls.movements

    @classmethod
    def stock_remains(cls):
        remains = []

        numbers_id = list(set(obj.product.pid for obj in cls.movements))
        for num in numbers_id:
            qty = cls.product_qty(product_id=num)
            remains.append([num, qty])

        return remains
