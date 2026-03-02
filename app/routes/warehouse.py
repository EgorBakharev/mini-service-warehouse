from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.db.session import get_db
from app.services.warehouse_service import add_warehouse, get_warehouse_by_id, get_warehouses, delete_warehouse

router = APIRouter(prefix="/warehouses", tags=["Warehouse"])


@router.post("")
def warehouse_create(warehouse_name: str, db: Session = Depends(get_db)):
    """ Эндпоинт, добавление склада """

    try:
        return add_warehouse(warehouse_name=warehouse_name, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.get("/{id}")
def warehouse_view(wid: int, db: Session = Depends(get_db)):
    """ Эндпоинт, получить склад """

    try:
        return get_warehouse_by_id(wid, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.get("")
def warehouse_list(db: Session = Depends(get_db)):
    """ Эндпоинт, получить список складов """

    return get_warehouses(db=db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def warehouse_delete(wid: int, db: Session = Depends(get_db)):
    """ Эндпоинт, настоящее удаление склада """

    try:
        delete_warehouse(wid, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)
