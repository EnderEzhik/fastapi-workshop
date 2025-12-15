from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models.product import ProductCreate, ProductUpdate, ProductOut
from app.repositories.products import (get_product_by_id,
                                       create_product as create_product_repo,
                                       update_product as update_product_repo)


router = APIRouter(prefix="/products", tags=["Products"])


# Получение продукта по ID
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(session: SessionDep, product_id: int):
    product = await get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Создаем новый продукт
@router.post("/", response_model=ProductOut)
async def create_product(session: SessionDep, product_create: ProductCreate):
    new_product = await create_product_repo(session=session, product_create=product_create)
    return new_product


# Полностью обновляем продукт
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(session: SessionDep, product_id: int, product_update: ProductUpdate):
    product_db = await get_product_by_id(session=session, product_id=product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = await update_product_repo(session=session, product_db=product_db, product_update=product_update)
    return updated_product
