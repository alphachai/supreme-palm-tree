import datetime
from enum import IntEnum
from typing import List

from pydantic import BaseModel

# Pizza Topping (many-to-many)
# class PizzaToppingBase(BaseModel):
#     pizza_id: int
#     topping_id: int
#
# class PizzaToppingCreate(PizzaToppingBase):
#     pass
#
# class PizzaTopping(PizzaToppingBase):
#     id: int
#
#     class Config:
#         orm_mode = True


# Pizza
class PizzaBase(BaseModel):
    toppings: list = []


class PizzaCreate(PizzaBase):
    order_id: int


class Pizza(PizzaBase):
    id: int
    # toppings: List[PizzaTopping] = []

    class Config:
        orm_mode = True


# Topping
# class ToppingBase(BaseModel):
#     name: str
#
# class ToppingCreate(ToppingBase):
#     pass
#
# class Topping(ToppingBase):
#     id: int
#     pizzas: List[PizzaTopping] = []
#
#     class Config:
#         orm_mode = True


# Order
class OrderBase(BaseModel):
    user_id: int
    timestamp: datetime.datetime


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    pizzas: List[Pizza] = []

    class Config:
        orm_mode = True


# Order Status
# Using an enum as a placeholder for a real model to simplify.
class Status(IntEnum):
    STARTED = 1
    SUBMITTED = 2
    PREPARING = 3
    OUT_FOR_DELIVERY = 4
    DELIVERED = 5
    READY_FOR_PICKUP = 6
    CANCELED = 7


class OrderStatusBase(BaseModel):
    status: int
    order_id: int


class OrderStatusCreate(OrderStatusBase):
    pass


class OrderStatus(OrderStatusBase):
    id: int

    class Config:
        orm_mode = True


# User
class UserBase(BaseModel):
    email: str = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int = None
    orders: List[Order] = []

    class Config:
        orm_mode = True
