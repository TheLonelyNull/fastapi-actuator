from fastapi import FastAPI

from fastapi_actuator.endpoints.endpoint import Endpoint


class HealthcheckEndpoint(Endpoint):
    def __init__(self):
        # TODO list of liveness and readiness checks
        pass

    def add_to_actuator(self, actuator_app: FastAPI) -> None:
        @actuator_app.get(
            "/health/readiness",
            tags=["Health"]
        )
        def evaluate_readiness():
            pass

        @actuator_app.get(
            "/health/liveness",
            tags=["Health"]
        )
        def evaluate_liveness():
            pass
