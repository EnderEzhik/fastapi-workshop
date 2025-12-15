from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.models.product import ProductCreate, ProductUpdate, ProductOut
import app.repositories.products as products_repo


router = APIRouter(prefix="/products", tags=["Products"])


# Получение продукта по ID
@router.get("/{product_id}", response_model=ProductOut)
async def get_product(session: SessionDep, product_id: int):
    product = await products_repo.get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Создаем новый продукт
@router.post("/", response_model=ProductOut)
async def create_product(session: SessionDep, product_create: ProductCreate):
    new_product = await products_repo.create_product(session, product_create)
    return new_product


# Полностью обновляем продукт
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(session: SessionDep, product_id: int, product_update: ProductUpdate):
    product_db = await products_repo.get_product_by_id(session, product_id)
    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = await products_repo.update_product(session, product_db, product_update)
    return updated_product
