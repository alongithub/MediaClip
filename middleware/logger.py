from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from infra.logger import logger


def getUserInfo(request: Request):
    return getattr(request.state, "user", None)


noAuthPath = [
    "/openapi.json",
    "/user/login",
    "/docs",
    "/internal.*"
]


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        body = await request.body()
        logger.debug(f"Request: {request.method} {request.url} - Body: {body.decode('utf-8')}")
        
        response = await call_next(request)
        # logger.debug(f"Response: {response.status_code} - Body: {response}")
        return response
