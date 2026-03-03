import pytest

from app.core.exceptions import MyError
from app.models.warehouse_model import WarehouseModel
from app.services.warehouse_service import add_warehouse, get_warehouse_by_id, get_warehouses, delete_warehouse


class TestWarehouseService:
    """Тесты для сервиса складов"""

    def test_add_warehouse(self, db_session):
        """Тест успешного добавления склада"""

        warehouse = add_warehouse("Склад-1", db=db_session)

        assert warehouse.id is not None
        assert warehouse.name == "Склад-1"

        db_warehouse = db_session.get(WarehouseModel, warehouse.id)

        assert db_warehouse.id is not None
        assert db_warehouse.name == "Склад-1"

    def test_add_warehouse_duplicate(self, db_session):
        """Тест добавления склада с дублирующимся именем"""

        add_warehouse("Склад-1", db=db_session)

        with pytest.raises(MyError) as my_error:
            add_warehouse("Склад-1", db=db_session)

        assert my_error.value.code == 400
        assert "уже существует" in my_error.value.message

    def test_get_warehouse_by_id(self, db_session, test_warehouse):
        """Тест успешного получения склада по ID"""

        warehouse = get_warehouse_by_id(test_warehouse.id, db=db_session)

        assert warehouse.id == test_warehouse.id
        assert warehouse.name == test_warehouse.name

    def test_get_warehouse_by_id_no(self, db_session):
        """Тест получения несуществующего склада"""

        with pytest.raises(MyError) as my_error:
            get_warehouse_by_id(0, db=db_session)

        assert my_error.value.code == 404
        assert "Склада нет" in my_error.value.message

    def test_get_warehouses(self, db_session, test_warehouse):
        """Тест получения списка всех складов"""

        warehouses = get_warehouses(db=db_session)

        assert len(warehouses) >= 1
        assert any(w.id == test_warehouse.id for w in warehouses)

    def test_delete_warehouse(self, db_session, test_warehouse):
        """Тест успешного удаления склада"""

        deleted_warehouse = delete_warehouse(test_warehouse.id, db=db_session)

        assert deleted_warehouse.id == test_warehouse.id

        db_warehouse = db_session.get(WarehouseModel, test_warehouse.id)
        assert db_warehouse is None