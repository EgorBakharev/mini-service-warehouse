from app.routes.product import router as products_router
from app.routes.warehouse import router as warehouses_router
from app.routes.movement import router as movements_router

__all__ = ["products_router", "warehouses_router", "movements_router"]
