from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.base import intpk


# Создаем таблицу склады
class WarehouseModel(Base):
    __tablename__ = 'warehouses'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)

    movements = relationship("MovementModel", back_populates="warehouse", cascade="all, delete-orphan")
