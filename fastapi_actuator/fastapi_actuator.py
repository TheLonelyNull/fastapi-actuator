from typing import Self

from fastapi import FastAPI

from fastapi_actuator.endpoints.endpoint import Endpoint
from fastapi_actuator.endpoints.healthchecks.healthcheck_endpoint import HealthcheckEndpoint
from fastapi_actuator.endpoints.info.info_endpoint import InfoEndpoint


class FastAPIActuator:
    def __init__(self, endpoints: list[Endpoint]):
        self._actuator_api = FastAPI()
        for endpoint in endpoints:
            endpoint.add_to_actuator(self._actuator_api)

    @classmethod
    def from_config(cls) -> Self:
        # TODO probable do the settings and shit here
        return FastAPIActuator(
            endpoints=[
                InfoEndpoint(),
                HealthcheckEndpoint(),
            ]
        )

    def mount_to_app(self, app: FastAPI) -> None:
        """Mount the actuator to the main FastAPI application.

        Args:
            app: The main FastAPI application to mount the actuator to.
        """
        app.mount("/actuator", self._actuator_api)


