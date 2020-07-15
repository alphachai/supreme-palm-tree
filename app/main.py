import logging
from datetime import datetime
from typing import Dict, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.db import SessionLocal

# Using alembic to create migrations which will be applied on container startup
# from app.db import session
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Supreme Palm Tree")
logger = logging.getLogger()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "ok"}


# Users
@app.post("/users/", response_model=Dict[str, schemas.User])
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    fields = {"email": user.email}
    return {"user": crud.create(db=db, model=models.User, **fields)}


@app.get("/users/", response_model=Dict[str, List[schemas.User]])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return {"users": crud.read(db, models.User, skip, limit)}


@app.get("/users/{id}/", response_model=Dict[str, schemas.User])
async def get_user(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.User).filter(models.User.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": obj}


@app.patch("/users/{id}/", response_model=Dict[str, schemas.User])
async def update_user(id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    if query.count() != 1:
        raise HTTPException(status_code=404, detail="User not found")
    crud.update(db, query, user)
    return {"user": query.first()}


# Orders
@app.post("/orders/", response_model=Dict[str, schemas.Order])
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    fields = {"user_id": order.user_id, "timestamp": datetime.utcnow()}
    return {"order": crud.create(db=db, model=models.Order, **fields)}


@app.get("/orders/", response_model=Dict[str, List[schemas.Order]])
async def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return {"orders": crud.read(db, models.Order, skip, limit)}


@app.get("/orders/status/")
async def get_order_status():
    return {"order_status": {s.value: s.name for s in schemas.Status}}


@app.get("/orders/{id}/", response_model=Dict[str, schemas.Order])
async def get_order(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Order).filter(models.Order.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order": obj}


@app.patch("/orders/{id}/", response_model=Dict[str, schemas.Order])
async def update_order(id: int, user: schemas.OrderBase, db: Session = Depends(get_db)):
    query = db.query(models.Order).filter(models.Order.id == id)
    if query.count() != 1:
        raise HTTPException(status_code=404, detail="Order not found")
    crud.update(db, query, order)
    return {"order": query.first()}


# In the real world, you'd probably want to update the order row directly during the process.
# @app.patch("/orders/{id}/", response_model=Dict[str, schemas.Order])
# async def update_order()


# Pizzas
@app.post("/pizzas/", response_model=Dict[str, schemas.Pizza])
async def create_pizza(pizza: schemas.PizzaCreate, db: Session = Depends(get_db)):
    fields = {"order_id": pizza.order_id, "toppings": pizza.toppings}
    return {"pizza": crud.create(db=db, model=models.Pizza, **fields)}


@app.get("/pizzas/", response_model=Dict[str, List[schemas.Pizza]])
async def get_pizzas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return {"pizzas": crud.read(db, models.Pizza, skip, limit)}


@app.get("/pizzas/toppings/")
async def get_pizza_toppings():
    return {"pizza_toppings": {t.value: t.name for t in schemas.Topping}}


@app.get("/pizzas/{id}/")
async def get_pizza(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Pizza).filter(models.Pizza.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Pizza not found")
    return {"pizza": obj}


# @app.get("/pizzas/", response_model=Dict[str, List[schemas.Pizza]])
# async def get_pizzas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return {"pizzas": crud.read(db, models.Pizza, skip, limit)}
#
#
# @app.get("/pizzas/{id}/", response_model=Dict[str, schemas.Pizza])
# async def get_pizza(id: int, db: Session = Depends(get_db)):
#     obj = db.query(models.Pizza).filter(models.Pizza.id == id).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return {"pizza": obj}
