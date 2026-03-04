import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.db.session import get_db
from app.models import ProductModel, WarehouseModel, MovementModel
from app.schemas.stock_scheme import MoveType

engine = create_engine("sqlite:///./test.db")

TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db_session():
    """
        Фикстура для создания сессии базы данных.
        Создаёт таблицы перед каждым тестом и удаляет после.
    """

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """
        Фикстура для создания тестового клиента FastAPI.
        Переопределяет зависимость get_db для использования тестовой БД.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_warehouse(db_session):
    """Фикстура для создания тестового склада"""

    warehouse = WarehouseModel(name="Склад-0")
    db_session.add(warehouse)
    db_session.commit()
    db_session.refresh(warehouse)

    return warehouse


@pytest.fixture
def test_product(db_session):
    """Фикстура для создания тестового продукта"""

    product = ProductModel(
        sku="sku-000",
        name="Coffee",
        description="Молотый, 250г",
        price=100.0
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


@pytest.fixture
def test_movement(db_session, test_product, test_warehouse):
    """Фикстура для создания тестового движения"""

    movement = MovementModel(
        product_id=test_product.id,
        warehouse_id=test_warehouse.id,
        type=MoveType.IN,
        qty=10,
        comment="Поставка"
    )
    db_session.add(movement)
    db_session.commit()
    db_session.refresh(movement)

    return movement
