from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.db.session import get_db
from app.services.warehouse_service import add_warehouse, get_warehouse_by_id, get_warehouses

router = APIRouter(prefix="/warehouses", tags=["Warehouse"])


# Эндпоинт, добавить склад
@router.post("")
def warehouse_create(warehouse_name: str, db: Session = Depends(get_db)):
    try:
        return add_warehouse(warehouse_name=warehouse_name, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


# Эндпоинт, получить склад
@router.get("/{id}")
def warehouse_view(wid: int, db: Session = Depends(get_db)):
    try:
        return get_warehouse_by_id(wid, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


# Эндпоинт, получить список складов
@router.get("")
def warehouse_list(db: Session = Depends(get_db)):
    return get_warehouses(db=db)

