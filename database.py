import datetime
from enum import Enum
from typing import Optional, Annotated

from sqlalchemy import create_engine, or_

from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy import CheckConstraint, func, Enum, text, select, ForeignKey, case
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.exc import IntegrityError
from app.schemas.product_scheme import ProductApp, ProductUpdate
from er import MyError
from app.schemas.stock_scheme import MoveType

engine = create_engine('sqlite:///my.db', echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]


class ProductBase(Base):
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


class WarehouseBase(Base):
    __tablename__ = 'warehouse'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)


class MovementBase(Base):
    __tablename__ = 'movement'

    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    warehouse_name: Mapped[str] = mapped_column(ForeignKey("warehouse.name"))
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


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


# class ProductBase(Base):
#     __tablename__ = "product"
#
#     id: Mapped[intpk]
#     sku: Mapped[str] = mapped_column(unique=True)
#     name: Mapped[str]
#     description: Mapped[Optional[str]]
#     price: Mapped[float] = mapped_column(CheckConstraint('price >= 0'))
#     created_at: Mapped[created_at]
#
#     def __repr__(self) -> str:
#         return (f"User(id={self.id!r}, "
#                 f"sku={self.sku!r}, "
#                 f"name={self.name!r}, "
#                 f"description={self.description!r}, "
#                 f"price={self.price!r}, "
#                 f"created_at={self.created_at!r})")


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


def random_products():
    with Session() as session:
        for i in range(1, 4):
            product = ProductBase(
                sku=f"SKU-{i:03d}",
                name=f"Товар {i}",
                description=f"Подробное описание товара номер {i}",
                price=round(100.0 + i * 15.5, 2),  # разные цены
            )
            session.add(product)
            session.commit()


# random_products()


def get_product_by_id(pid: int):
    with Session() as session:
        result = session.get(ProductBase, pid)

        if result is None:
            raise MyError(code=404, message='Товара нет')

        return result


def get_products(limit: int = 20, offset: int = 0, search: str = None):
    with Session() as session:
        stmt = select(ProductBase)
        if search:
            stmt = stmt.where(
                or_(
                    ProductBase.sku.ilike(f"%{search}%"),
                    ProductBase.name.ilike(f"%{search}%")  # ileke соусоу
                )
            )

        stmt = stmt.offset(offset).limit(limit)

        return session.execute(stmt).scalars().all()


def add_product(app: ProductApp):
    with Session() as session:
        session_product = ProductBase(
            sku=app.sku,
            name=app.name,
            description=app.description,
            price=app.price
        )

        session.add(session_product)
        try:
            session.commit()

        except IntegrityError:
            session.rollback()  # нужен ли для всех исключений
            raise MyError(code=400, message=f"{app.sku} уже существует")

        return session_product


def update_product(pid: int, prod_up: ProductUpdate):
    with Session() as session:
        if isinstance(prod_up.price, (int, float)) and prod_up.price < 0:
            raise MyError(code=400, message='Цена меньше 0.0')

        existing_product = get_product_by_id(pid)
        update_data = prod_up.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_product, field, value)

        session.commit()

        return existing_product


def delete_product(pid: int):
    with Session() as session:
        session_product = get_product_by_id(pid)

        if session_product:
            session.delete(session_product)
            session.commit()

        return session_product


# Stock
from app.schemas.stock_scheme import MovementApp


def prim():
    with Session() as session:
        wer = WarehouseBase(name="Склад-1")
        session.add(wer)
        session.commit()


# prim()


def add_move(move: MovementApp):
    with Session() as session:
        if move.qty <= 0:
            raise MyError(code=422, message="Движение не может быть отрицательным или нулевым")

        qty_now = product_qty(move.product_id)

        if qty_now < move.qty and move.type == MoveType.OUT:
            raise MyError(400, f"Недостаточно товара на складе. Количество {qty_now}")

        res = MovementBase(**move.model_dump())
        session.add(res)
        session.commit()


def product_qty(product_id: int) -> int:
    get_product_by_id(product_id)

    with Session() as session:
        stmt = select(
            func.coalesce(
                func.sum(
                    case(
                        (MovementBase.type == MoveType.IN, MovementBase.qty),
                        (MovementBase.type == MoveType.OUT, -MovementBase.qty),
                        else_=0
                    )
                ), 0
            )
        ).where(MovementBase.product_id == product_id)

        total_qty = session.execute(stmt).scalar()
        return total_qty


def stock_movements(warehouse_name: str):
    with Session() as session:
        res = select(MovementBase).filter(MovementBase.warehouse_name == warehouse_name)
        result = session.scalars(res).all()

        return result


def stock_remains():
    ...


#print(stock_remains)

