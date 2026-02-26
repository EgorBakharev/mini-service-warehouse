from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models import ProductModel

from app.schemas.product_scheme import ProductApp, ProductUpdate

from er import MyError


def get_product_by_id(pid: int):
    with SessionLocal() as session:
        result = session.get(ProductModel, pid)

        if result is None:
            raise MyError(code=404, message='Товара нет')

        return result


def get_products(limit: int = 20, offset: int = 0, search: str = None):
    with SessionLocal() as session:
        stmt = select(ProductModel)
        if search:
            stmt = stmt.where(
                or_(
                    ProductModel.sku.ilike(f"%{search}%"),
                    ProductModel.name.ilike(f"%{search}%")  # ileke соусоу
                )
            )

        stmt = stmt.offset(offset).limit(limit)

        return session.execute(stmt).scalars().all()


def add_product(app: ProductApp):
    with SessionLocal() as session:
        session_product = ProductModel(
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
    with SessionLocal() as session:
        if isinstance(prod_up.price, (int, float)) and prod_up.price < 0:
            raise MyError(code=400, message='Цена меньше 0.0')

        existing_product = get_product_by_id(pid)
        update_data = prod_up.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(existing_product, field, value)

        session.commit()

        return existing_product


def delete_product(pid: int):
    with SessionLocal() as session:
        session_product = get_product_by_id(pid)

        if session_product:
            session.delete(session_product)
            session.commit()

        return session_product
