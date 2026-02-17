from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field

from er import MyError


# Модель которую заполняют
class ProductApp(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float = Field(0.0, ge=0.0)


# Модель для частичного обновления (все поля необязательные)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class Product(BaseModel):
    pid: int
    sku: str
    name: str
    description: str = "Описание товара"
    price: float = Field(0.0, ge=0.0)
    created_at: datetime = Field(default_factory=datetime.now)

    @staticmethod
    def get_product_by_id(pid: int):
        for product in products_list:
            if product.pid == pid:
                return product
        raise MyError(code=404, message='Товара нет')

    @classmethod
    def product_add(cls, app: ProductApp):

        for prod in products_list:
            if app.sku == prod.sku:
                raise MyError(code=400, message=f"{app.sku} уже существует")

        product = cls(
            id=len(products_list) + 1,
            name=app.name,
            sku=app.sku,
            description=app.description,
            price=app.price
        )

        products_list.append(product)
        return product

    @classmethod
    def product_remove(cls, pid: int):
        product = cls.get_product_by_id(pid=pid)
        products_list.remove(product)

    @classmethod
    def product_receive(cls, pid: int):
        return cls.get_product_by_id(pid=pid)

    @classmethod
    def product_change(cls, pid: int, product_update: ProductUpdate):

        if isinstance(product_update.price,  (int, float)) and product_update.price < 0:
            raise MyError(code=400, message='Цена меньше 0.0')

        existing_product = cls.get_product_by_id(pid=pid)
        update_data = product_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_product, field, value)

        return existing_product

    @classmethod
    def product_list(cls, limit: int = 20, offset: int = 0, search: str = None):

        if search:
            search_lower = search.lower()
            result = []

            for prod in products_list:
                if search_lower in prod.sku.lower() or search_lower in prod.name.lower():
                    result.append(prod)
            return result[offset: offset + limit]

        return products_list[offset: offset + limit]


def random_products():
    products: List[Product] = []
    base_time = datetime.now()

    for i in range(1, 3):
        product = Product(
            pid=i,  # задаём уникальный id
            name=f"Товар {i}",
            sku=f"SKU-{i:03d}",  # например, SKU-001
            description=f"Подробное описание товара номер {i}",
            price=round(100.0 + i * 15.5, 2),  # разные цены
            created_at=base_time - timedelta(days=i)  # разные даты
        )
        products.append(product)
    return products


products_list = random_products()
# print(products_list)

