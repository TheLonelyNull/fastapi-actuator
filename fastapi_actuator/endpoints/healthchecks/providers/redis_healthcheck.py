from typing import TYPE_CHECKING

from fastapi_actuator.endpoints.healthchecks.healthcheck import Healthcheck, HealthStatus, HealthcheckResponse
from fastapi_actuator.errors import InvalidHealthcheckDependencyError

if TYPE_CHECKING:
    try:
        from redis import Redis as SyncRedis
        from redis.asyncio import Redis as AsyncRedis
    except ImportError:
        raise InvalidHealthcheckDependencyError(
            "Redis must be installed to use type checking with the redis healthcheck."
        )


class RedisHealthcheck(Healthcheck):
    def __init__(self, redis: "SyncRedis", name: str = "redis"):
        self._redis = redis
        self._name = name

    def get_name(self) -> str:
        return self._name

    async def get_status(self) -> HealthcheckResponse:
        try:
            response = self._redis.ping()
            if response:
                info = self._redis.info()
                return HealthcheckResponse(
                    status=HealthStatus.UP,
                    details={
                        "version": info["redis_version"],
                        "mode": info["redis_mode"]
                    }
                )
            else:
                return HealthcheckResponse(
                    status=HealthStatus.DOWN,
                    details={
                        "reason": "Ping was unsuccessful."
                    }
                )

        except Exception as e:
            return HealthcheckResponse(
                status=HealthStatus.DOWN,
                details={
                    "reason": str(e)
                }
            )


class AsyncRedisHealthcheck(Healthcheck):
    def __init__(self, redis: "AsyncRedis", name: str = "redis"):
        self._redis = redis
        self._name = name

    def get_name(self) -> str:
        return self._name

    async def get_status(self) -> HealthcheckResponse:
        try:
            response = await self._redis.ping()
            if response:
                info = await self._redis.info()
                return HealthcheckResponse(
                    status=HealthStatus.UP,
                    details={
                        "version": info["redis_version"],
                        "mode": info["redis_mode"]
                    }
                )
            else:
                return HealthcheckResponse(
                    status=HealthStatus.DOWN,
                    details={
                        "reason": "Ping was unsuccessful."
                    }
                )
        except Exception as e:
            return HealthcheckResponse(
                status=HealthStatus.DOWN,
                details={
                    "reason": str(e)
                }
            )
