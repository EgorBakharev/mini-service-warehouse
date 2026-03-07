from typing import Optional

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.base import intpk, created_at


# Создаем таблицу продукты
class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    sku: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[float] = mapped_column(CheckConstraint('price >= 0'))
    created_at: Mapped[created_at]

    movements = relationship("MovementModel", back_populates="product")
