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
    def from_config(cls, readiness_checks: list | None = None, liveness_checks: list | None = None) -> Self:
        # TODO probable do the settings and shit here
        return FastAPIActuator(
            endpoints=[
                InfoEndpoint(),
                HealthcheckEndpoint(
                    readiness_checks=[] if readiness_checks is None else readiness_checks,
                    liveness_checks=[] if liveness_checks is None else liveness_checks
                ),
            ]
        )

    def mount_to_app(self, app: FastAPI) -> None:
        """Mount the actuator to the main FastAPI application.

        Args:
            app: The main FastAPI application to mount the actuator to.
        """
        app.mount("/actuator", self._actuator_api)
