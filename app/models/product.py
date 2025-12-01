from sqlalchemy import Column, Integer, Float, String, Boolean

from pydantic import BaseModel, Field

from app.models import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    in_stock = Column(Boolean, default=True, nullable=False)


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    price: float = Field(ge=0)
    in_stock: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=128)
    price: float | None = Field(default=None, ge=0)
    in_stock: bool | None = None


class ProductOut(ProductBase):
    id: int
    model_config = { "from_attributes": True }
