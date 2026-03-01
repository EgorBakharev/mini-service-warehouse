from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

from app.models import ProductModel, WarehouseModel, MovementModel

from app.routes import products_router, warehouse_router, movement_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Service")

app.include_router(products_router)
app.include_router(warehouse_router)
app.include_router(movement_router)


@app.get("/")
def root():
    return {"message": "Welcome to Warehouse API"}