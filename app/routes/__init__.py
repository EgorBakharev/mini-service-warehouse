from app.routes.product import router as products_router
from app.routes.warehouse import router as warehouse_router
from app.routes.movement import router as movement_router

__all__ = ["products_router", "warehouse_router", "movement_router"]
