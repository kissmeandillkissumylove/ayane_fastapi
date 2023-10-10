"""
10.09.2023 https://github.com/kissmeandillkissumylove
"""

from datetime import datetime
from typing import Union, Optional
from enum import Enum
from fastapi import FastAPI, Request, status
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field

users = [
    {
        "id": 0,
        "role": "admin",
        "name": "Alice"
    },
    {
        "id": 1,
        "role": "farmer",
        "name": "Mike"
    },
    {
        "id": 2,
        "role": "driver",
        "name": "Anna"
    },
    {
        "id": 3,
        "role": "programmer",
        "name": "Gorge"
    },
    {
        "id": 4,
        "role": "signalman",
        "name": "Luci",
        "degree": [{
            "id": 1,
            "created_at": "2020-01-01T00:00:00",
            "type_degree": "expert",
        }]
    },
]

trades = [
    {
        "id": 0,
        "user_id": 2,
        "price": 123,
        "pcs": 35,
        "currency": "USD"
    },
    {
        "id": 1,
        "user_id": 2,
        "price": 523,
        "pcs": 15,
        "currency": "USD"
    },
    {
        "id": 2,
        "user_id": 2,
        "price": 752,
        "pcs": 78,
        "currency": "USD"
    },
    {
        "id": 3,
        "user_id": 2,
        "price": 53,
        "pcs": 54,
        "currency": "USD"
    },
    {
        "id": 4,
        "user_id": 2,
        "price": 578,
        "pcs": 23,
        "currency": "USD"
    },
    {
        "id": 5,
        "user_id": 2,
        "price": 273,
        "pcs": 75,
        "currency": "USD"
    },
    {
        "id": 6,
        "user_id": 2,
        "price": 895,
        "pcs": 53,
        "currency": "USD"
    },
]


class App(object):
    """app with fastapi class."""
    app = FastAPI()  # create app


class Trade(BaseModel):
    """custom data type for trades."""
    id: int
    user_id: int
    price: float = Field(ge=0)
    pcs: float
    currency: str = Field(max_length=5)


class DegreeType(Enum):
    """custom data type for Degree class."""
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    """custom data type for user degree."""
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    """custom data type for user."""
    id: int
    role: str
    name: str
    degree: Optional[list[Degree]] = None


@App.app.exception_handler(ValidationException)
async def validation_exception_handler(
        request: Request,
        exc: ValidationException):
    """function for handling validation-related errors. returns an error to
    the client that occurred NOT because of the client, but because of the
    server. it is used if we trust the client and can show errors that occur
    on the server."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


@App.app.get("/")
def sam(a: Union[int, float] = 20, b: Union[int, float] = 20) -> Union[int, float]:
    """sum of two variables. complexity: O(1)."""
    return a + b


@App.app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int) -> dict:
    """returns user id."""
    return users[user_id]


@App.app.get("/trades")
def get_trades(limit: int = 5) -> list:
    """get 5 trades from end."""
    return trades[-limit:]


@App.app.patch("/users/{user_id}")
def change_username(user_id: int, new_name: str) -> dict:
    """change username."""
    users[user_id]["name"] = new_name
    return {"status": 200, "data": users[user_id]}


@App.app.post("/trades")
def add_trades(new_trades: list[Trade]) -> dict:
    """add new trades in to list."""
    trades.extend(new_trades)
    return {"status": 200, "data": trades}
