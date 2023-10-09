from typing import Union
from fastapi import FastAPI

users = [
    {"id": 0, "role": "admin", "name": "Alice"},
    {"id": 1, "role": "farmer", "name": "Mike"},
    {"id": 2, "role": "driver", "name": "Anna"},
    {"id": 3, "role": "programmer", "name": "Gorge"},
    {"id": 4, "role": "signalman", "name": "Luci"}
]

trades = [
    {"id": 0, "user_id": 2, "price": 123, "pcs": 35},
    {"id": 1, "user_id": 2, "price": 523, "pcs": 15},
    {"id": 2, "user_id": 2, "price": 752, "pcs": 78},
    {"id": 3, "user_id": 2, "price": 53, "pcs": 54},
    {"id": 4, "user_id": 2, "price": 578, "pcs": 23},
    {"id": 5, "user_id": 2, "price": 273, "pcs": 75},
    {"id": 6, "user_id": 2, "price": 895, "pcs": 53},
]


class App(object):
    """app with fastapi class."""
    app = FastAPI()  # create app


@App.app.get("/")
def sam(a: Union[int, float] = 20, b: Union[int, float] = 20) -> Union[int, float]:
    """sum of two variables. complexity: O(1)."""
    return a + b


@App.app.get("/users/{user_id}")
def get_user(user_id: int) -> dict:
    """returns user id."""
    return users[user_id]


@App.app.get("/trades")
def get_trades(limit: int = 5):
    """get 5 trades from end."""
    return trades[-limit:]


@App.app.patch("/users/{user_id}")
def change_username(user_id: int, new_name: str):
    """change username."""
    users[user_id]["name"] = new_name
    return {"status": 200, "data": users[user_id]}
