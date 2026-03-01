from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.base import intpk


# Создаем таблицу склады
class WarehouseModel(Base):
    __tablename__ = 'warehouses'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
