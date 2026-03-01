from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.models import ProductModel
from app.schemas.product_scheme import ProductApp, ProductUpdate, ProductResponse


# Получить продукт
def get_product_by_id(pid: int, db: Session):
    result = db.get(ProductModel, pid)

    if result is None:
        raise MyError(code=404, message='Товара нет')

    return result


# Получить продукты
def get_products(db: Session, limit: int = 20, offset: int = 0, search: str = None):
    stmt = select(ProductModel)

    if search:
        stmt = stmt.where(
            or_(
                ProductModel.sku.ilike(f"%{search}%"),
                ProductModel.name.ilike(f"%{search}%")
            )
        )
    stmt = stmt.offset(offset).limit(limit)

    return db.execute(stmt).scalars().all()


# Добавить продукт
def add_product(app: ProductApp, db: Session):
    if app.price < 0:
        raise MyError(code=400, message=f"Цена продукта должна быть не меньше 0.")

    db_product = ProductModel(
        sku=app.sku,
        name=app.name,
        description=app.description,
        price=app.price
    )

    db.add(db_product)

    try:
        db.commit()
        db.refresh(db_product)
        return db_product

    except IntegrityError:
        db.rollback()
        raise MyError(code=400, message=f"{app.sku} уже существует")


# Частично изменить продукт
def update_product(pid: int, prod_up: ProductUpdate, db: Session):
    if isinstance(prod_up.price, (int, float)) and prod_up.price < 0:
        raise MyError(code=400, message='Цена меньше 0.0')

    existing_product = get_product_by_id(pid, db=db)
    update_data = prod_up.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_product, field, value)

    db.commit()
    db.refresh(existing_product)

    return existing_product


# Удалить продукт (настоящее удаление)
def delete_product(pid: int, db: Session):
    session_product = get_product_by_id(pid, db=db)

    if session_product:
        db.delete(session_product)
        db.commit()

    return session_product
