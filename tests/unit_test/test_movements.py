import pytest

from app.core.exceptions import MyError
from app.models.movement_model import MovementModel
from app.schemas.stock_scheme import MovementApp, MoveType
from app.services.movement_service import add_move, product_qty, movements_warehouse, remains_warehouse


class TestMovementService:
    """Тесты для сервиса движений"""

    def test_add_move(self, db_session, test_product, test_warehouse):
        """Тест успешного добавления прихода"""

        move_app = MovementApp(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            type=MoveType.IN,
            qty=10,
            comment="Приход"
        )

        movement = add_move(move_app, db=db_session)

        assert movement.id is not None
        assert movement.qty == 10
        assert movement.type == MoveType.IN
        assert movement.created_at is not None

        db_movement = db_session.get(MovementModel, movement.id)

        assert db_movement.id is not None
        assert db_movement.qty == 10
        assert db_movement.type == MoveType.IN
        assert db_movement.created_at is not None

    def test_add_move_zero_qty(self, db_session, test_product, test_warehouse):
        """Тест добавления движения с нулевым количеством"""

        move_app = MovementApp(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            type=MoveType.IN,
            qty=0
        )

        with pytest.raises(MyError) as my_error:
            add_move(move_app, db_session)

        assert my_error.value.code == 422
        assert "Движение не может быть" in my_error.value.message

    def test_add_move_out_insufficient_qty(self, db_session, test_product, test_warehouse):
        """Тест расхода при недостаточном количестве"""

        move_in = MovementApp(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            type=MoveType.IN,
            qty=5
        )
        add_move(move_in, db=db_session)

        move_out = MovementApp(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            type=MoveType.OUT,
            qty=10
        )

        with pytest.raises(MyError) as my_error:
            add_move(move_out, db=db_session)

        assert my_error.value.code == 400
        assert "Недостаточно товара" in my_error.value.message

    def test_product_qty(self, db_session, test_product, test_warehouse):
        """Тест расчёта остатка товара"""

        move_in = MovementApp(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            type=MoveType.IN,
            qty=100
        )
        add_move(move_in, db=db_session)

        move_out = MovementApp(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            type=MoveType.OUT,
            qty=30
        )
        add_move(move_out, db=db_session)

        qty = product_qty(test_product.id, test_warehouse.id, db=db_session)

        assert qty == 70

    def test_movements_warehouse(self, db_session, test_movement, test_warehouse):
        """Тест получения всех движений склада"""

        movements = movements_warehouse(test_warehouse.id, db=db_session)

        assert len(movements) >= 1
        assert any(m.id == test_movement.id for m in movements)

    def test_remains_warehouse(self, db_session, test_product, test_warehouse):
        """Тест получения остатков (только положительные)"""

        move_in = MovementApp(
            product_id=test_product.id,
            warehouse_id=test_warehouse.id,
            type=MoveType.IN,
            qty=50
        )
        add_move(move_in, db=db_session)

        remains = remains_warehouse(test_warehouse.id, db=db_session)

        assert len(remains) >= 1
        assert any(r["product_id"] == test_product.id and r["qty"] > 0 for r in remains)
