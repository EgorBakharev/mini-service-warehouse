from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.base import intpk


class WarehouseModel(Base):
    __tablename__ = 'warehouse'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
