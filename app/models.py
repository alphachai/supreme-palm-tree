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
    status_id = Column(Integer)
    pizzas = relationship("Pizza")


class Pizza(Base):
    __tablename__ = "pizza"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    toppings = Column("data", postgresql.ARRAY(Integer))
    # toppings = relationship("PizzaTopping")


# Ideally, this should be a many to many relationship
# Status <- OrderStatus -> Order
# We'd want to track the throughput of orders. Alternatively, you could store
# status directly on the order row and track performance / throughput another way.
# Possibly via audit logging or simply prometheus metrics (since we likely care
# more about aggregate performance than individual orders when reviewing
# performance.)
#
# class OrderStatus(Base):
#     __tablename__ = "order_status_update"
#     id = Column(Integer, primary_key=True, index=True)
#     order_id = Column(Integer, ForeignKey("order.id"))
#     timestamp = Column(types.TIMESTAMP)
#     status = Column(Integer)
#
# See app.schemas.Status(IntEnum)
# class OrderStatusType(Base):
#     __tablename__ = "order_status_type"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)


# Axing these in favor of an enum to save time.
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
