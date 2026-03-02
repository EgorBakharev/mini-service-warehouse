from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.models import ProductModel
from app.schemas.product_scheme import ProductApp, ProductUpdate


def get_product_by_id(pid: int, db: Session):
    """
        Получить продукт по ID.

        Args:
            pid (int): Уникальный ID.
            db (Session): Cессия.

        Returns:
            ProductModel: Объект модели продукта.

        Raises:
            MyError: Код 404, если продукт с указанным ID не найден.
    """

    result = db.get(ProductModel, pid)

    if result is None:
        raise MyError(code=404, message='Товара нет')

    return result


def get_products(db: Session, limit: int = 20, offset: int = 0, search: str = None):
    """
        Получить список продуктов.

        Поиск осуществляется по полям `sku` и `name`.

        Args:
            db (Session): Сессия.
            limit (int): Максимальное количество записей для возврата. По умолчанию: 20.
            offset (int): Смещение начала выборки. По умолчанию: 0.
            search (Optional[str]): Поисковый запрос по артикулу или названию.

        Returns:
            List[ProductModel]: Список объектов моделей продуктов.
    """

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


def add_product(app: ProductApp, db: Session):
    """
        Добавить новый продукт в бд.

        Проверяет корректность цены и уникальность артикула (SKU).

        Args:
            app (ProductApp): Схема данных для создания продукта.
            db (Session): Сессия.

        Returns:
            ProductModel: Созданный объект модели продукта (с ID и created_at).

        Raises:
            MyError: Код 400, если цена меньше 0 или SKU уже существует.
    """

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


def update_product(pid: int, prod_up: ProductUpdate, db: Session):
    """
        Частично обновить данные существующего продукта.

        Обновляются только те поля, которые были переданы в схеме обновления.

        Args:
            pid (int): Уникальный ID.
            prod_up (ProductUpdate): Схема данных с новыми значениями полей.
            db (Session): Сессия.

        Returns:
            ProductModel: Обновлённый объект модели продукта.

        Raises:
            MyError: Код 400, если цена меньше 0.
            MyError: Код 404, если продукт не найден.
    """

    if isinstance(prod_up.price, (int, float)) and prod_up.price < 0:
        raise MyError(code=400, message='Цена меньше 0.0')

    existing_product = get_product_by_id(pid, db=db)
    update_data = prod_up.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_product, field, value)

    db.commit()
    db.refresh(existing_product)

    return existing_product


def delete_product(pid: int, db: Session):
    """
        Удалить продукт из базы данных (постоянное удаление).

        Args:
            pid (int): Уникальный ID.
            db (Session): Сессия.

        Returns:
            ProductModel: Удалённый объект модели продукта.

        Raises:
            MyError: Код 404, если продукт не найден.
    """

    session_product = get_product_by_id(pid, db=db)

    if session_product:
        db.delete(session_product)
        db.commit()

    return session_product
