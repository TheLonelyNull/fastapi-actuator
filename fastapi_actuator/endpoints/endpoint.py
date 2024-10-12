from typing import Protocol

from fastapi import FastAPI


class Endpoint(Protocol):
    def add_to_actuator(self, actuator_app: FastAPI) -> None:
        raise NotImplementedError()
