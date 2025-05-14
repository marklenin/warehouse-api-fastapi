from pydantic import BaseModel
from typing import List
from datetime import datetime
from .models import OrderStatus


#Product
class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    quantity_in_warehouse: int

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass


#Order
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    title: str
    price: float
    
    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItem]

    class Config: 
        orm_mode = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus