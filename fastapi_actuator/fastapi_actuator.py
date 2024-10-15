from typing import Self

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from fastapi_actuator.endpoints.endpoint import Endpoint
from fastapi_actuator.endpoints.healthchecks.healthcheck import Healthcheck
from fastapi_actuator.endpoints.healthchecks.healthcheck_endpoint import HealthcheckEndpoint
from fastapi_actuator.endpoints.info.info_endpoint import InfoEndpoint


class InfoConfig(BaseModel):
    enabled: bool = True
    extra: dict = {}


class HealthcheckConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    readiness_enabled: bool = True
    liveness_enabled: bool = True
    readiness_checks: list[Healthcheck] = []
    liveness_checks: list[Healthcheck] = []


class FastAPIActuatorConfig(BaseModel):
    info_config: InfoConfig = InfoConfig()
    healthcheck_config: HealthcheckConfig = HealthcheckConfig()


class FastAPIActuator:
    def __init__(self, endpoints: list[Endpoint]):
        self._actuator_api = FastAPI()
        for endpoint in endpoints:
            endpoint.add_to_actuator(self._actuator_api)

    @classmethod
    def from_config(cls, config: FastAPIActuatorConfig) -> Self:
        enabled_endpoints = []
        if config.info_config.enabled:
            enabled_endpoints.append(
                InfoEndpoint(
                    extra=config.info_config.extra
                )
            )

        if config.healthcheck_config.readiness_enabled or config.healthcheck_config.liveness_enabled:
            enabled_endpoints.append(
                HealthcheckEndpoint(
                    readiness_checks=config.healthcheck_config.readiness_checks if config.healthcheck_config.readiness_enabled else None,
                    liveness_checks=config.healthcheck_config.liveness_checks if config.healthcheck_config.liveness_enabled else None
                )
            )

        return FastAPIActuator(
            endpoints=enabled_endpoints
        )

    def mount_to_app(self, app: FastAPI) -> None:
        """Mount the actuator to the main FastAPI application.

        Args:
            app: The main FastAPI application to mount the actuator to.
        """
        app.mount("/actuator", self._actuator_api)
