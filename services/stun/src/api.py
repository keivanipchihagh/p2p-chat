import redis
from typing import List
import uvicorn
from http import HTTPStatus
from fastapi import FastAPI
from fastapi import Request, Response

# Third-party imports
from config import (
    # API
    API_HOST,
    API_PORT,
    API_LOG_LEVEL,
    API_RELOAD,
    API_WORKERS,
    # Redis
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_DB,
)

APP = FastAPI()
REDIS = redis.Redis(
    host = REDIS_HOST,
    port = REDIS_PORT,
    password = REDIS_PASSWORD,
    db = REDIS_DB,
    decode_responses = True
)


@APP.get(
    "/api/readiness",
    tags = ["healthcheck", "readiness"],
    summary = "Readiness Probe",
    status_code = HTTPStatus.OK,
)
def readiness():
    # Readiness probe
    return {"status": "ok"}



@APP.get(
    "/api/liveness",
    tags = ["healthcheck", "liveness"],
    summary = "Liveness Probe",
    status_code = HTTPStatus.OK,
)
def liveness():
    # Liveness probe
    return {"status": "ok"}



@APP.post(
    "/api/v1/register",
    tags = ["v1", "register"],
    status_code = HTTPStatus.CREATED,
)
async def register(request: Request):
    data: dict = await request.json()

    username: str   = data.get('username')
    host: str       = data.get('host')
    port: str       = data.get('port')

    if not username or not host or not port:
        # Check if username, host and port are provided
        return Response(
            content = '{error: "provide required fields."}',
            status_code = HTTPStatus.BAD_REQUEST
        )

    if REDIS.exists(username):
        # Check if user already exists
        return Response(
            content = '{error: "username is taken."}',
            status_code = HTTPStatus.CONFLICT
        )

    REDIS.hset(
        username,
        mapping = {"host": host, "port": port}
    )

    return data



@APP.get("/api/v1/peers")
async def peers():
    peers: List[str] = REDIS.keys("*")
    return peers



@APP.get("/api/v1/peerinfo")
async def peerinfo(request: Request):
    username: str = request.query_params.get('username')

    if not REDIS.exists(username):
        # Check if user exists
        return Response(
            content = '{error: "username does not exist."}',
            status_code = HTTPStatus.NOT_FOUND
        )

    return REDIS.hgetall(username)



if __name__ == "__main__":

    # Run API server (blocking)
    uvicorn.run(
        app = "api:APP",
        host = API_HOST,
        port = API_PORT,
        log_level = API_LOG_LEVEL,
        workers = API_WORKERS,
        reload = API_RELOAD,
    )
