from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import MyError
from app.models import WarehouseModel


# Добавить склад
def add_warehouse(warehouse_name: str, db: Session):
    warehouse = WarehouseModel(name=warehouse_name)
    db.add(warehouse)

    try:
        db.commit()
        db.refresh(warehouse)
        return warehouse

    except IntegrityError:
        db.rollback()
        raise MyError(code=400, message=f"Склад: '{warehouse_name}' уже существует")


# Получить склад
def get_warehouse_by_id(wid: int, db: Session):
    result = db.get(WarehouseModel, wid)

    if result is None:
        raise MyError(code=404, message='Склада нет')

    return result


# Получить список складов
def get_warehouses(db: Session):
    return db.execute(select(WarehouseModel)).scalars().all()
