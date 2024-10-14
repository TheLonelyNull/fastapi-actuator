from enum import StrEnum
from typing import Protocol, Self

from pydantic import BaseModel, ConfigDict, Field


class HealthStatus(StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


class HealthcheckResponse(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    status: HealthStatus
    details: dict = Field(default_factory=dict)
    components: dict[str, Self] = Field(default_factory=dict)


class Healthcheck(Protocol):
    def get_name(self) -> str:
        raise NotImplementedError()

    async def get_status(self) -> HealthcheckResponse:
        raise NotImplementedError()
