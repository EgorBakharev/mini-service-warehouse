from fastapi import FastAPI, HTTPException, status

from app.schemas.product_scheme import ProductApp, ProductUpdate
from app.schemas.stock_scheme import MovementApp, StockResponse

from er import MyError
from product import Product
from stock import Warehouse, Movement

import database

app = FastAPI()
wr_h1 = Warehouse(name="Главный склад")


@app.post("/products")
def product_create(product: ProductApp):
    try:
        return database.add_product(product)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/products")
def products_list(limit: int = 20, offset: int = 0, search: str = None):
    return database.get_products(limit=limit, offset=offset, search=search)


@app.get("/products/{id}")
def product_view(pid: int):
    try:
        return database.get_product_by_id(pid)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.patch("/products/{id}")
def product_patch(pid: int, product_update: ProductUpdate):
    try:
        return database.update_product(pid, prod_up=product_update)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT)
def product_delete(pid: int):
    try:
        database.delete_product(pid)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get('/stock/remains')
def stock_remains():
    result = [StockResponse(product_id=elem[0], qty=elem[1]) for elem in wr_h1.stock_remains()]
    return result


@app.get("/stock/movements/{warehouse_name}")
def stock_movements(warehouse_name: str):
    return database.stock_movements(warehouse_name)


@app.post("/stock/movement", status_code=status.HTTP_204_NO_CONTENT)
def stock_movement(move: MovementApp):
    try:
        return database.add_move(move=move)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/stock/{product_id}")
def stock(product_id: int):
    try:
        return StockResponse(product_id=product_id, qty=database.product_qty(product_id=product_id))

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)
