from sqlalchemy import Column, ForeignKey, Integer, String, types
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    orders = relationship("Order")


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    timestamp = Column(types.TIMESTAMP)
    pizzas = relationship("Pizza")


class OrderStatus(Base):
    __tablename__ = "order_status_update"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    timestamp = Column(types.TIMESTAMP)
    status = Column(Integer)


# I suspect this basically never changes, so an enum is probably enough to start.
# ..partially because I'm avoiding writing more endpoints for this demo.
# See app.schemas.Status(IntEnum)
# class OrderStatusType(Base):
#     __tablename__ = "order_status_type"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)


class Pizza(Base):
    __tablename__ = "pizza"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    toppings = Column("data", postgresql.ARRAY(Integer))
    # toppings = relationship("PizzaTopping")


# Axing these to save time.
# class Topping(Base):
#     __tablename__ = "topping"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     pizzas = relationship("PizzaTopping")
#
#
# class PizzaTopping(Base):
#     __tablename__ = "pizza_topping"
#     id = Column(Integer, primary_key=True, index=True)
#     pizza_id = Column(Integer, ForeignKey("pizza.id"))
#     topping_id = Column(Integer, ForeignKey("topping.id"))
