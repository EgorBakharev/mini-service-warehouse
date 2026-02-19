from fastapi import FastAPI, HTTPException, status

from product import Product, ProductUpdate, MyError, ProductApp
from stock import Warehouse, MovementApp, StockResponse, Movement

app = FastAPI()
wh_01 = Warehouse(1)

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


@app.get("/stock/list")
def stock_movements():
    try:
        return wh_01.movements
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.post("/stock/movement", status_code=status.HTTP_204_NO_CONTENT)
def stock_movement(move: MovementApp):
    try:
        moveObject = Movement(move.product_id, move.qty, move.type, move.comment)
        return wh_01.add_move(move=moveObject)
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@app.get("/stock/{product_id}")
def stock(product_id: int):
    try:
        qty = wh_01.product_qty(product_id=product_id)
        return StockResponse(product_id=product_id, qty=qty)
    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)

# from pydantic import BaseModel
# class User(BaseModel):
#     username: str
#     email: str
#     password: str # Скрываемое поле
#
# class UserResponse(BaseModel):
#     username: str
#     email: str # Оставляем только нужные поля
#
# @app.get("/user", response_model=UserResponse)
# def get_user(user: User):
#     # return {"username": "user1", "email": "a@b.com", "password": "secret_password"}
#     return user