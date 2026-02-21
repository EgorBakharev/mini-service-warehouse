from fastapi import FastAPI, HTTPException, status

from scheme_product import ProductApp, ProductUpdate
from scheme_stock import MovementApp, StockResponse

from er import MyError
from product import Product
from stock import Warehouse, Movement

app = FastAPI()


@app.post("/products")
def product_create(product: ProductApp):
    try:
        return Product.product_add(product)

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


@app.get('/stock/remains')
def stock_remains():
    result = [StockResponse(product_id=elem[0], qty=elem[1]) for elem in Warehouse.stock_remains()]
    return result


@app.get("/stock/movements")
def stock_movements():
    try:
        return Warehouse.movements

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.post("/stock/movement", status_code=status.HTTP_204_NO_CONTENT)
def stock_movement(move: MovementApp):
    try:
        return Warehouse.add_move(move=Movement(move.product_id, move.qty, move.type, move.comment))

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/stock/{product_id}")
def stock(product_id: int):
    try:
        qty = Warehouse.product_qty(product_id=product_id)
        return StockResponse(product_id=product_id, qty=qty)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)
