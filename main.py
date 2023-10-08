from typing import Union
from fastapi import FastAPI


class App(object):
    """app with fastapi class."""
    app = FastAPI()  # create app


@App.app.get("/")
def sam(a: Union[int, float] = 20, b: Union[int, float] = 20) -> Union[int, float]:
    """sum of two variables. complexity: O(1)."""
    return a + b
