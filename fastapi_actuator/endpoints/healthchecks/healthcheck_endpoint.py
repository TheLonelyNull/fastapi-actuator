from typing import Collection

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from fastapi_actuator.endpoints.endpoint import Endpoint
from fastapi_actuator.endpoints.healthchecks.healthcheck import Healthcheck, HealthStatus, HealthcheckResponse


class HealthcheckEndpoint(Endpoint):
    def __init__(self,
                 readiness_checks: list[Healthcheck],
                 liveness_checks: list[Healthcheck]
                 ) -> None:
        self._readiness_checks = readiness_checks
        self._liveness_checks = liveness_checks

    def add_to_actuator(self, actuator_app: FastAPI) -> None:
        @actuator_app.get(
            "/health/readiness",
            tags=["Health"],
            response_model_exclude_unset=True
        )
        async def evaluate_readiness() -> HealthcheckResponse:
            statuses = await self._evaluate_readiness()
            return self._generate_response(statuses)

        @actuator_app.get(
            "/health/liveness",
            tags=["Health"],
            response_model_exclude_unset=True
        )
        async def evaluate_liveness() -> HealthcheckResponse:
            statuses = await self._evaluate_liveness()
            return self._generate_response(statuses)

    async def _evaluate_readiness(self):
        return {check.get_name(): await check.get_status() for check in self._readiness_checks}

    async def _evaluate_liveness(self):
        return {check.get_name(): await check.get_status() for check in self._liveness_checks}

    @classmethod
    def _generate_response(cls, statuses: dict[str, HealthcheckResponse]) -> HealthcheckResponse:
        aggregate_status = cls._get_aggregate_status(statuses.values())
        return HealthcheckResponse(
                status=aggregate_status,
                components=statuses
            # status_code=status.HTTP_200_OK if aggregate_status == HealthStatus.UP
            #                                   or aggregate_status == HealthStatus.UNKNOWN
            # else status.HTTP_503_SERVICE_UNAVAILABLE
        )

    @classmethod
    def _get_aggregate_status(cls, statuses: Collection[HealthcheckResponse]) -> HealthStatus:
        if statuses and all(s.status == HealthStatus.UP for s in statuses):
            return HealthStatus.UP
        if statuses and any(s.status == HealthStatus.DOWN for s in statuses):
            return HealthStatus.DOWN
        return HealthStatus.UNKNOWN
