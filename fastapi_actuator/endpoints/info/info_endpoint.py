import platform
import sys

from fastapi import FastAPI

from fastapi_actuator.endpoints.endpoint import Endpoint


class InfoEndpoint(Endpoint):

    def add_to_actuator(self, actuator_app: FastAPI) -> None:
        @actuator_app.get(
            "/info",
            tags=["Info"]
        )
        def return_application_information():
            return {
                "python": {
                    "name": platform.python_implementation(),
                    "version": platform.python_version()
                }
            }
