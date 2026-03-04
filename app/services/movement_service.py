from typing import Sequence, List, Dict, Any

from sqlalchemy import select, func, case
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.models import MovementModel
from app.schemas.stock_scheme import MovementApp, MoveType
from app.services.product_service import get_product_by_id
from app.services.warehouse_service import get_warehouse_by_id


def add_move(move: MovementApp, db: Session) -> MovementModel:
    """
        Добавить движение.

        Проверяет наличие достаточного количества товара на складе
        при операции расхода (OUT).

        Args:
            move (MovementApp): Схема данных для создания движения.
            db (Session): Сессия.

        Returns:
            MovementModel: Созданный объект модели движения (с ID и created_at).

        Raises:
            MyError: Код 422, если количество товара <= 0.
            MyError: Код 400, если недостаточно товара на складе при расходе.
    """

    if move.qty <= 0:
        raise MyError(code=422, message="Движение не может быть отрицательным или нулевым")

    qty_now = product_qty(move.product_id, move.warehouse_id, db=db)

    if qty_now < move.qty and move.type == MoveType.OUT:
        raise MyError(400, f"Недостаточно товара на складе. Количество {qty_now}")

    res = MovementModel(**move.model_dump())

    db.add(res)
    db.commit()
    db.refresh(res)

    return res


def product_qty(product_id: int, warehouse_id: int, db: Session) -> int:
    """
         Рассчитать текущий остаток товара на складе.

         Вычисляет разницу между всеми приходами (IN) и расходами (OUT)
         для указанного продукта на указанном складе.

         Args:
             product_id (int): Уникальный ID продукта.
             warehouse_id (int): Уникальный ID склада.
             db (Session): Сессия.

         Returns:
             int: Текущее количество товара на складе.

         Raises:
             MyError: Код 404, если продукт или склад не найдены.
     """

    get_product_by_id(product_id, db)
    get_warehouse_by_id(warehouse_id, db)

    qty_expression = func.sum(
        case(
            (MovementModel.type == "IN", MovementModel.qty),
            (MovementModel.type == "OUT", -MovementModel.qty),
            else_=0
        )
    )

    stmt = select(qty_expression).where(
        MovementModel.product_id == product_id,
        MovementModel.warehouse_id == warehouse_id
    )

    total_qty = db.execute(stmt).scalar()

    return total_qty if total_qty else 0


def movements_warehouse(warehouse_id: int, db: Session) -> Sequence[MovementModel]:
    """
        Получить все движения для указанного склада.

        Args:
            warehouse_id (int): Уникальный ID склада.
            db (Session): Cессия.

        Returns:
            Sequence[MovementModel]: Список объектов моделей движения.

        Raises:
            MyError: Код 404, если склад не найден.
    """

    get_warehouse_by_id(warehouse_id, db)

    stmt = select(MovementModel).filter(MovementModel.warehouse_id == warehouse_id)
    result = db.scalars(stmt).all()

    return result


def remains_warehouse(warehouse_id: int, db: Session) -> List[Dict[str, Any]]:
    """
        Получить текущие остатки всех товаров на указанном складе.

        Возвращает только товары с положительным остатком (qty > 0).

        Args:
            warehouse_id (int): Уникальный ID склада.
            db (Session): Сессия.

        Returns:
            List[Dict[str, Any]]: Список словарей с product_id и qty.
                                  Пример: [{"product_id": 1, "qty": 50}, ...]

        Raises:
            MyError: Код 404, если склад не найден.
    """

    get_warehouse_by_id(warehouse_id, db)

    qty_expression = func.sum(
        case(
            (MovementModel.type == "IN", MovementModel.qty),
            (MovementModel.type == "OUT", -MovementModel.qty),
            else_=0
        )
    )

    stmt = select(
        MovementModel.product_id,
        qty_expression
    ).where(
        MovementModel.warehouse_id == warehouse_id
    ).group_by(
        MovementModel.product_id
    ).having(
        qty_expression > 0
    )

    results = db.execute(stmt).all()

    return [
        {"product_id": row[0], "qty": row[1]}
        for row in results
    ]
