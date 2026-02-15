from typing import List

from fastapi import FastAPI, HTTPException, status
from datetime import datetime, timedelta
from pydantic import BaseModel, Field


# Подправить класс чуть позже
class Product(BaseModel):
    id: int  # авто
    sku: str  # нужна уникальная строка
    name: str
    escription: str = "Описание товара"  # может быть пустой
    price: float = 0.0  # не меньше 0.0
    created_at: datetime  # дата/время авто

    def product_list(self):



# переименовать переменные
def random_products():
    # Создаём список из 10 объектов Product
    products: List[Product] = []
    base_time = datetime.now()

    for i in range(1, 21):
        product = Product(
            id=i,  # задаём уникальный id
            name=f"Товар {i}",
            sku=f"SKU-{i:03d}",  # например, SKU-001
            description=f"Подробное описание товара номер {i}",
            price=round(100.0 + i * 15.5, 2),  # разные цены
            created_at=base_time - timedelta(days=i)  # разные даты
        )
        products.append(product)
    return products


products = random_products()

app = FastAPI()
"""
Правила которые нужно сделать

1. Нельзя создать товар с таким же sku, если он уже есть.

2. Нельзя сделать OUT, если на складе не хватает товара.

3. Остаток товара не может стать отрицательным.

4. Нельзя создать движение для товара, которого нет.
"""


# исправить чтобы в запросе не было id и created_at
"""
доделать 

Ответ: созданный товар (с id и created_at).

Ошибки:
sku уже существует → 400 или 409
"""
@app.post("/products")
def product_create(product: Product):

    return products.append(product)


@app.get("/products")
def products_list(limit: int = 20, offset: int = 0, search: str = None): # limit and search сделать
    if search:
        search_lower = search.lower()
        result = []

        for prod in products:
            if search_lower in prod.sku.lower() or search_lower in prod.name.lower():
                result.append(prod)
        return result[offset:limit]

    return products[offset:limit]


@app.get("/products/{id}")
def product_view(id: int):
    for product in products:
        if product.id == id:
            return product

    raise HTTPException(status_code=404, detail=f"Товара нет {id}")


@app.patch("/products/{id}")
def product_patch(id: int):
    ...


@app.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT)
def product_delete(id: int):
    for product in products:
        if product.id == id:
            products.remove(product)
            return

    raise HTTPException(status_code=404, detail="Товара нет")
