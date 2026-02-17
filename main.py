from fastapi import FastAPI, HTTPException, status

from product import Product, ProductUpdate, MyError, ProductApp
from warehouse import Warehouse, MovementApp, StockResponse

app = FastAPI()
"""
Правила которые нужно сделать
2. Нельзя сделать OUT, если на складе не хватает товара.

3. Остаток товара не может стать отрицательным.

4. Нельзя создать движение для товара, которого нет.
"""


@app.post("/products")
def product_create(product: ProductApp):
    try:
        new_product = Product.product_add(product)
        return new_product
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/products")
def products_list(limit: int = 20, offset: int = 0, search: str = None):
    return Product.product_list(limit=limit, offset=offset, search=search)


@app.get("/products/{id}")
def product_view(pid: int):
    try:
        return Product.product_receive(pid)
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.patch("/products/{id}")
def product_patch(pid: int, product_update: ProductUpdate):
    try:
        return Product.product_change(pid, product_update=product_update)
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT)
def product_delete(pid: int):
    try:
        Product.product_remove(pid)
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.post("/stock/movements")
def stock_movements(move: MovementApp):
    try:
        return Warehouse.add_movement(move=move)
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/stock/{product_id}")
def stock(product_id: int):
    try:
        qty = Warehouse.remainder_product(product_id=product_id)
        return StockResponse(product_id=product_id, qty=qty)
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)