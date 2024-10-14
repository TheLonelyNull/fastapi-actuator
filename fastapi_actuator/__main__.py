from fastapi import FastAPI
from redis import Redis
from redis.asyncio import Redis as ARedis


from fastapi_actuator.endpoints.healthchecks.providers.redis_healthcheck import RedisHealthcheck, AsyncRedisHealthcheck
from fastapi_actuator.fastapi_actuator import FastAPIActuator

redis = Redis()
aredis = ARedis()
redis.info()

app = FastAPI()

actuator = FastAPIActuator.from_config(
    readiness_checks=[
        RedisHealthcheck(redis),
        AsyncRedisHealthcheck(aredis, name="async redis"),
    ]
)
actuator.mount_to_app(app)

