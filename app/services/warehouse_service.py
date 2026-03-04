from typing import Optional, Type, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import MyError
from app.models import WarehouseModel


def add_warehouse(warehouse_name: str, db: Session) -> WarehouseModel:
    """
        Добавить новый склад в БД.

        Проверяет уникальность названия склада.

        Args:
            warehouse_name (str): Название нового склада.
            db (Session): Сессия.

        Returns:
            WarehouseModel: Созданный объект модели склада (с ID).

        Raises:
            MyError: Код 400, если склад с таким названием уже существует.
    """

    warehouse = WarehouseModel(name=warehouse_name)
    db.add(warehouse)

    try:
        db.commit()
        db.refresh(warehouse)
        return warehouse

    except IntegrityError:
        db.rollback()
        raise MyError(code=400, message=f"Склад: '{warehouse_name}' уже существует")


def get_warehouse_by_id(wid: int, db: Session) -> Optional[Type[WarehouseModel]]:
    """
        Получить склад по ID.

        Args:
            wid (int): Уникальный ID склада.
            db (Session): Сессия.

        Returns:
            Optional[Type[WarehouseModel]]: Объект модели склада или None.

        Raises:
            MyError: Код 404, если склад с указанным ID не найден.
    """

    result = db.get(WarehouseModel, wid)

    if result is None:
        raise MyError(code=404, message='Склада нет')

    return result


def get_warehouses(db: Session) -> Sequence[WarehouseModel]:
    """
         Получить список всех складов.

         Args:
             db (Session): Сессия.

         Returns:
             Sequence[WarehouseModel]: Список объектов моделей складов.
     """

    return db.execute(select(WarehouseModel)).scalars().all()


def delete_warehouse(wid: int, db: Session) -> Optional[Type[WarehouseModel]]:
    """
        Удалить склад из базы данных (постоянное удаление).

        Args:
            wid (int): Уникальный ID склада.
            db (Session): Сессия.

        Returns:
            Optional[Type[WarehouseModel]]: Удалённый объект модели склада или None.

        Raises:
            MyError: Код 404, если склада не найден.
    """

    session_warehouse = get_warehouse_by_id(wid, db=db)

    if session_warehouse:
        db.delete(session_warehouse)
        db.commit()

    return session_warehouse
