from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, order


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product.router)
app.include_router(order.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}