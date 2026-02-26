from app.db.session import SessionLocal
from app.models import WarehouseModel


def add_warehouse():
    with SessionLocal() as session:
        war = WarehouseModel(name="Склад-1")
        session.add(war)
        session.commit()
