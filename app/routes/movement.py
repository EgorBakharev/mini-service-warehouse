from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.db.session import get_db
from app.schemas.stock_scheme import MovementApp, StockResponse, MovementResponse
from app.services.movement_service import add_move, remains_warehouse, movements_warehouse, product_qty

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.get("/remains/{warehouse_id}", response_model=list[StockResponse])
def stock_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    """ Эндпоинт, получить текущие остатки всех товаров на указанном складе """

    try:
        result = remains_warehouse(warehouse_id, db=db)
        return result

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.get("/movements/{warehouse_id}", response_model=list[MovementResponse])
def history_movements(warehouse_id: int, db: Session = Depends(get_db)):
    """ Эндпоинт, получить все движения для указанного склада"""

    try:
        result = movements_warehouse(warehouse_id, db=db)
        return result

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.post("/movement", response_model=MovementResponse)
def stock_movement(move: MovementApp, db: Session = Depends(get_db)):
    """ Эндпоинт, добавить движение"""

    try:
        result = add_move(move=move, db=db)
        return result

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.get("/{product_id}", response_model=StockResponse)
def stock_product(product_id: int, db: Session = Depends(get_db), warehouse_id: int = 1):
    """ Эндпоинт, получить текущий остаток товара на складе """

    try:
        qty = product_qty(product_id=product_id, warehouse_id=warehouse_id, db=db)

        return StockResponse(
            product_id=product_id,
            qty=qty
        )

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)
