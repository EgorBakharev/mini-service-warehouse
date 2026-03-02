from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import MyError
from app.db.session import get_db
from app.schemas.product_scheme import ProductApp, ProductUpdate, ProductResponse
from app.services.product_service import add_product, get_products, get_product_by_id, update_product, delete_product

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse)
def product_create(product: ProductApp, db: Session = Depends(get_db)):
    """ Эндпоинт, создание товара """

    try:
        return add_product(product, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.get("", response_model=list[ProductResponse])
def products_list(limit: int = 20, offset: int = 0, search: Optional[str] = None, db: Session = Depends(get_db)):
    """ Эндпоинт, получить товары """

    return get_products(limit=limit, offset=offset, search=search, db=db)


@router.get("/{id}", response_model=ProductResponse)
def product_view(pid: int, db: Session = Depends(get_db)):
    """ Эндпоинт, получить товар """

    try:
        result = get_product_by_id(pid, db=db)
        return result

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.patch("/{id}", response_model=ProductResponse)
def product_patch(pid: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """ Эндпоинт, частичное измение товара """

    try:
        return update_product(pid, prod_up=product_update, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def product_delete(pid: int, db: Session = Depends(get_db)):
    """ Эндпоинт, настоящее удаление товара """

    try:
        delete_product(pid, db=db)

    except MyError as my_error:
        raise HTTPException(status_code=my_error.code, detail=my_error.message)
