from sqlalchemy import select, func, case
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.models.movement_model import MovementModel
from app.schemas.stock_scheme import MovementApp, MoveType
from app.services.product_service import get_product_by_id
from app.services.warehouse_service import get_warehouse_by_id


# Добавление движения
def add_move(move: MovementApp, db: Session):
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


# Считает остаток товара
def product_qty(product_id: int, warehouse_id: int, db: Session) -> int:
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


# Движения по складу
def movements_warehouse(warehouse_id: int, db: Session):
    get_warehouse_by_id(warehouse_id, db)

    stmt = select(MovementModel).filter(MovementModel.warehouse_id == warehouse_id)
    result = db.scalars(stmt).all()

    return result


# Остаток товаров для склада
def remains_warehouse(warehouse_id: int, db: Session):
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

    return results
