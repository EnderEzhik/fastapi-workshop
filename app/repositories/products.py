from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product, ProductCreate, ProductUpdate


async def create_product(session: AsyncSession,
                         product_create: ProductCreate) -> Product:
    product_data = product_create.model_dump()
    new_product = Product(**product_data)
    session.add(new_product)
    await session.commit()
    return new_product


async def update_product(session: AsyncSession,
                         product_db: Product,
                         product_update: ProductUpdate) -> Product:
    product_data = product_update.model_dump(exclude_unset=True)
    for field, value in product_data.items():
        setattr(product_db, field, value)
    await session.commit()
    return product_db


async def get_product_by_id(session: AsyncSession,
                            product_id: int) -> Product | None:
    return await session.get(Product, product_id)
