from fastapi import FastAPI

from fastapi_actuator.fastapi_actuator import FastAPIActuator


app = FastAPI()

actuator = FastAPIActuator.from_config()
actuator.mount_to_app(app)

