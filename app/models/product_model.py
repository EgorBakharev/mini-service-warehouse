from typing import Optional

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.base import intpk, created_at


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[intpk]
    sku: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[float] = mapped_column(CheckConstraint('price >= 0'))
    created_at: Mapped[created_at]

    def __repr__(self) -> str:
        return (f"User(id={self.id!r}, "
                f"sku={self.sku!r}, "
                f"name={self.name!r}, "
                f"description={self.description!r}, "
                f"price={self.price!r}, "
                f"created_at={self.created_at!r})")
