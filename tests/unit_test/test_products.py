import pytest
from pydantic import ValidationError

from app.core.exceptions import MyError
from app.models.product_model import ProductModel
from app.schemas.product_scheme import ProductApp, ProductUpdate
from app.services.product_service import add_product, get_product_by_id, get_products, update_product, delete_product


class TestProductService:
    """Тесты для сервиса продуктов"""

    def test_add_product(self, db_session):
        """Тест успешного добавления продукта"""

        product_app = ProductApp(
            sku="sku-001",
            name="Apple",
            description="Золотистые",
            price=100.0
        )

        product = add_product(product_app, db=db_session)

        assert product.id is not None
        assert product.sku == "sku-001"
        assert product.name == "Apple"
        assert product.price == 100.0
        assert product.created_at is not None

        db_producr = db_session.get(ProductModel, product.id)

        assert db_producr.id is not None
        assert db_producr.sku == "sku-001"
        assert db_producr.name == "Apple"
        assert db_producr.price == 100.0
        assert db_producr.created_at is not None

    def test_add_product_negative_price(self, db_session):
        """Тест добавления продукта с отрицательной ценой"""

        ...

    def test_add_product_duplicate_sku(self, db_session, test_product):
        """Тест добавления продукта с дублирующимся SKU"""

        product_app = ProductApp(
            sku=test_product.sku,
            name="Tea",
            price=200.0
        )

        with pytest.raises(MyError) as my_error:
            add_product(product_app, db=db_session)

        assert my_error.value.code == 400
        assert "уже существует" in my_error.value.message

    def test_get_product_by_id(self, db_session, test_product):
        """Тест успешного получения продукта по ID"""

        product = get_product_by_id(test_product.id, db=db_session)

        assert product.id == test_product.id
        assert product.sku == test_product.sku

    def test_get_product_by_id_no(self, db_session):
        """Тест получения несуществующего продукта"""

        with pytest.raises(MyError) as my_error:
            get_product_by_id(0, db=db_session)

        assert my_error.value.code == 404
        assert "Товара нет" in my_error.value.message

    def test_update_product_name(self, db_session, test_product):
        """Тест успешного обновления продукта"""

        update_data = ProductUpdate(name="Milk")

        updated_product = update_product(test_product.id, update_data, db=db_session)

        assert updated_product.name == "Milk"

    def test_update_product_price(self, db_session, test_product):
        """Тест успешного обновления продукта"""

        update_data = ProductUpdate(price=150.0)

        updated_product = update_product(test_product.id, update_data, db=db_session)

        assert updated_product.price == 150.0

    def test_update_product_description(self, db_session, test_product):
        """Тест успешного обновления продукта"""

        update_data = ProductUpdate(description="Вкусно")

        updated_product = update_product(test_product.id, update_data, db=db_session)

        assert updated_product.description == "Вкусно"

    def test_delete_product(self, db_session, test_product):
        """Тест успешного удаления продукта"""

        deleted_product = delete_product(test_product.id, db=db_session)

        assert deleted_product.id == test_product.id

        db_product = db_session.get(ProductModel, test_product.id)
        assert db_product is None

    @pytest.mark.parametrize("search", ['sku', 'Coffee'])
    def test_get_products(self, db_session, test_product, search):
        """Тест поиска продуктов"""

        products = get_products(db=db_session, search=search)

        assert len(products) >= 1
        assert any(p.id == test_product.id for p in products)
