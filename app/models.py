from .database import Base
import enum
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Float, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity_in_warehouse = Column(Integer, nullable=False)


class OrderStatus(enum.Enum):
    delivered = "delivered"
    sent = "sent"
    pending = "pending"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="items")