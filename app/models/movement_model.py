from typing import Optional

from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.base import intpk, created_at
from app.schemas.stock_scheme import MoveType


# Создаем таблицу движения
class MovementModel(Base):
    __tablename__ = 'movements'

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"), index=True)
    type: Mapped[MoveType]
    qty: Mapped[int] = mapped_column(CheckConstraint('qty > 0'))
    comment: Mapped[Optional[str]]
    created_at: Mapped[created_at]

