import platform
import sys

from fastapi import FastAPI

from fastapi_actuator.endpoints.endpoint import Endpoint


class InfoEndpoint(Endpoint):
    def __init__(self, extra: dict):
        self._extra = extra

    def add_to_actuator(self, actuator_app: FastAPI) -> None:
        @actuator_app.get(
            "/info",
            tags=["Info"]
        )
        def return_application_information():
            info = {
                "python": {
                    "name": platform.python_implementation(),
                    "version": platform.python_version()
                }
            }
            info.update(self._extra)
            return info
