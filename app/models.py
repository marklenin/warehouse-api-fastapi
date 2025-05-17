from .database import Base
import enum
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Float, Enum, BigInteger, UniqueConstraint, Index
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped

from datetime import date

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    quantity_in_warehouse: Mapped[int] = mapped_column(Integer, nullable=False)



class OrderStatus(enum.Enum):
    delivered = "delivered"
    sent = "sent"
    pending = "pending"

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index("index_orders_created_at", "created_at"),
    )

    id:Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), server_default=text('now()'))
    status: Mapped[str] = mapped_column(Enum(OrderStatus), default=OrderStatus.pending)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__=(
        UniqueConstraint("order_id", "product_id", name="unique_pair_order_and_product"), 
        Index("index_order_and_product", "product_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(Integer)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")