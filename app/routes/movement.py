from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.db.session import get_db
from app.schemas.stock_scheme import MovementApp, StockResponse
from app.services.movement_service import add_move, remains_warehouse, movements_warehouse, product_qty

router = APIRouter(prefix="/stock", tags=["Stock"])


# Эндпоинт, получить остаток товаров по складу
@router.get("/remains/{warehouse_id}")
def stock_warehouse(warehouse_id: int, db: Session = Depends(get_db)):
    result = remains_warehouse(warehouse_id, db=db)
    return [StockResponse(product_id=elem[0], qty=elem[1]) for elem in result]


# Эндпоинт, получить историю движения по складу
@router.get("/movements/{warehouse_id}")
def hustory_movements(warehouse_id: int, db: Session = Depends(get_db)):
    return movements_warehouse(warehouse_id, db=db)


# Эндпоинт, добавить движение по складу
@router.post("/movement", status_code=status.HTTP_204_NO_CONTENT)
def stock_movement(move: MovementApp, db: Session = Depends(get_db)):
    try:
        add_move(move=move, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


# Эндпоинт, получить остаток товара на складе
@router.get("/{product_id}", response_model=StockResponse)
def stock_product(
        product_id: int,
        db: Session = Depends(get_db),
        warehouse_id: int = 1

):
    try:
        qty = product_qty(product_id=product_id, warehouse_id=warehouse_id, db=db)

        return StockResponse(
            product_id=product_id,
            qty=qty
        )

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)
