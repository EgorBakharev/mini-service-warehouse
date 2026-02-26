from sqlalchemy import select, func, case

from app.db.session import SessionLocal
from app.models import MovementModel
from app.schemas.stock_scheme import MovementApp, MoveType
from app.services.product_service import get_product_by_id

from er import MyError


def add_move(move: MovementApp):
    with SessionLocal() as session:
        if move.qty <= 0:
            raise MyError(code=422, message="Движение не может быть отрицательным или нулевым")

        qty_now = product_qty(move.product_id, move.warehouse_id)

        print(f" {qty_now} {move.qty}")
        if qty_now < move.qty and move.type == MoveType.OUT:
            raise MyError(400, f"Недостаточно товара на складе. Количество {qty_now}")

        res = MovementModel(**move.model_dump())
        session.add(res)
        session.commit()


def product_qty(product_id: int, warehouse_id: int) -> int:
    get_product_by_id(product_id)

    with SessionLocal() as session:
        stmt = select(
            func.sum(
                case(
                    (MovementModel.type == MoveType.IN, MovementModel.qty),
                    (MovementModel.type == MoveType.OUT, -MovementModel.qty),
                    else_=0
                )
            )
        ).where(
            MovementModel.product_id == product_id
        ).group_by(
            MovementModel.warehouse_id
        ).having(
            MovementModel.warehouse_id == warehouse_id
        )

        total_qty = session.scalar(stmt)
        return total_qty if isinstance(total_qty, int) else 0


def stock_movements(warehouse_id: int):
    with SessionLocal() as session:
        res = select(MovementModel).filter(MovementModel.warehouse_id == warehouse_id)
        result = session.scalars(res).all()

        return result


def stock_remains(warehouse_id: int):
    with SessionLocal() as session:
        qty_expression = func.sum(
            case(
                (MovementModel.type == MoveType.IN, MovementModel.qty),
                (MovementModel.type == MoveType.OUT, -MovementModel.qty),
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

        results = session.execute(stmt).all()

        return results
