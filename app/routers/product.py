from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

#Get all products
@router.get("/", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


#Get one product
@router.get("/{id}", response_model=schemas.Product)
def get_product(id:int, db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with this id: {id} dose not exist")
    
    return product

#Create
@router.post("/", response_model=schemas.ProductCreate, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db:Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

#Update
@router.put("/{id}", response_model=schemas.Product)
def update_product(id: int, product: schemas.ProductCreate, db:Session = Depends(get_db)):
   
    product_query = db.query(models.Product).filter(models.Product.id == id)

    if not product_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} dose not exist")
    
    product_query.update(product.dict(), synchronize_session=False)
    db.commit()

    return product_query.first()

#Delete
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int, db:Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)

    if product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id: {id} dose not exist")

    product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)