from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.base import intpk, created_at

from app.schemas.stock_scheme import MoveType


class MovementModel(Base):
    __tablename__ = 'movement'

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), index=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), index=True)
    type: Mapped[MoveType]
    qty: Mapped[int]
    comment: Mapped[Optional[str]]
    created_at: Mapped[created_at]

    def __repr__(self) -> str:
        return (f"User(id={self.id!r}, "
                f"product_id={self.product_id!r}, "
                f"type={self.type!r}, "
                f"comment={self.comment!r}, "
                f"qty={self.qty!r}, "
                f"created_at={self.created_at!r})")
