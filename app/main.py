from fastapi import FastAPI, HTTPException, status, Query

from app.db.base import Base
from app.db.session import engine
from app.schemas.product_scheme import ProductApp, ProductUpdate
from app.schemas.stock_scheme import MovementApp, StockResponse
from app.services import product_service
from app.services import movement_service
# from app.services import warehouse_service
from er import MyError

app = FastAPI()


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.post("/products")
def product_create(product: ProductApp):
    try:
        return product_service.add_product(product)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/products")
def products_list(limit: int = 20, offset: int = 0, search: str = None):
    return product_service.get_products(limit=limit, offset=offset, search=search)


@app.get("/products/{id}")
def product_view(pid: int):
    try:
        return product_service.get_product_by_id(pid)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.patch("/products/{id}")
def product_patch(pid: int, product_update: ProductUpdate):
    try:
        return product_service.update_product(pid, prod_up=product_update)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT)
def product_delete(pid: int):
    try:
        product_service.delete_product(pid)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get('/stock/remains/{warehouse_id}')
def stock_remains(warehouse_id: int):
    result = [StockResponse(product_id=elem[0], qty=elem[1]) for elem in movement_service.stock_remains(warehouse_id)]
    return result


@app.get("/stock/movements/{warehouse_id}")
def stock_movements(warehouse_id: int):
    return movement_service.stock_movements(warehouse_id)


@app.post("/stock/movement", status_code=status.HTTP_204_NO_CONTENT)
def stock_movement(move: MovementApp):
    try:
        return movement_service.add_move(move=move)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/stock/{product_id}")
def stock(product_id: int, warehouse_id: int = Query(..., description="Название склада")):
    try:
        return StockResponse(product_id=product_id,
                             qty=movement_service.product_qty(product_id=product_id, warehouse_id=warehouse_id))

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)
