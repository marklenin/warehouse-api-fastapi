from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, joinedload
from typing import List
from .. import models, schemas
from ..database import get_db
from .product import get_product

router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

#Get all
@router.get("/", response_model = List[schemas.Order])
def get_orders(db:Session = Depends(get_db)):
    orders = db.query(models.Order).options(joinedload(models.Order.items).joinedload(models.OrderItem.product)).all()
    return orders


#Get one
@router.get("/{id}", response_model=schemas.Order)
def get_order(id:int, db:Session=Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == id).first()
    return order


#Create
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(new_order:schemas.OrderCreate, db: Session = Depends(get_db)):
    items = new_order.items
    for item in items:
        product = get_product(item.product_id,db)
        if not product or product.quantity_in_warehouse<item.quantity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail=f"Not enough quantity for product with id: {item.product_id}")

    order = models.Order()
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in items:
        product = get_product(item.product_id, db)
        product.quantity_in_warehouse -= item.quantity
        db_item = models.OrderItem(order_id = order.id, product_id=item.product_id, quantity=item.quantity)
        db.add(db_item)
    
    db.commit()
    db.refresh(order)
    return order


#Update
@router.patch("/{id}/status", response_model=schemas.Order)
def update_orders_status(id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    order = get_order(id, db)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
   
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    
    return order
