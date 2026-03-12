"""
DevOps Info Service
Main application module
"""

# Imports
import os
import socket
import platform
import logging
import json
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi import FastAPI, Request, Response


# Setting up logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger()
logger.addHandler(handler)


if os.getenv('DEBUG', 'false') == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


# Setting up pydantic structures
class SystemInfo(BaseModel):
    hostname: str
    platform: str
    platform_version: str
    architecture: str
    python_version: str


class ServiceInfo(BaseModel):
    name:        str
    version:     str
    description: str
    framework:   str


class UptimeInfo(BaseModel):
    uptime_seconds: int
    uptime_human:   str
    current_time:   str
    timezone:       str


class RequestInfo(BaseModel):
    client_ip:  str
    user_agent: str
    method:     str
    path:       str


class EndpointInfo(BaseModel):
    path:        str
    method:      str
    description: str


class MainEndpoint(BaseModel):
    system:    SystemInfo
    service:   ServiceInfo
    runtime:   UptimeInfo
    request:   RequestInfo
    endpoints: list[EndpointInfo]


class HealthEndpoint(BaseModel):
    status:         str
    timestamp:      str
    uptime_seconds: int


# Various information collecting functions
def get_system_info():
    """Collect system information."""
    return SystemInfo(
        hostname=socket.gethostname(),
        platform=platform.system(),
        platform_version=platform.version(),
        architecture=platform.machine(),
        python_version=platform.python_version()
    )


def get_service_info():
    """Collect service information."""
    return ServiceInfo(
        name=app.title,
        version=app.version,
        description=app.description,
        framework="fastapi",
    )


def get_uptime():
    delta = datetime.now() - start_time
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return UptimeInfo(
        uptime_seconds=seconds,
        uptime_human=f"{hours} hours, {minutes} minutes",
        current_time=datetime.now(timezone.utc).isoformat(),
        timezone=str(timezone.utc),
    )


def get_endpoints():
    return [
        EndpointInfo(
            path="/",
            method="GET",
            description="Service information",
        ),
        EndpointInfo(
            path="/health",
            method="GET",
            description="Health check",
        ),
    ]


# Application start time
logger.info("Application starting...")
START_TIME = datetime.now(timezone.utc)
start_time = datetime.now()

app = FastAPI(
    title="DevOps Info Service",
    description="DevOps course info service",
    summary="",
    version="0.1.1",
)


# Logging
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    logger.info(f'Request: {request.method} {request.url.path}')
    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    logger.info(f'Response code: {response.status_code}.')
    return Response(content=response_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type)


# FastAPI
@app.get("/")
def index(request: Request):
    """Main endpoint - service and system information."""
    logger.info("Collecting general information...")
    return MainEndpoint(
        system=get_system_info(),
        service=get_service_info(),
        runtime=get_uptime(),
        request=RequestInfo(
            client_ip=request.client.host,
            user_agent=request.headers.get("user-agent"),
            method=request.method,
            path=request.url.path,
        ),
        endpoints=get_endpoints(),
    )


@app.get("/health")
def health(request: Request):
    """Health endpoint - information about services status"""
    logger.info("Collecting service health information...")
    uptime_info = get_uptime()
    return HealthEndpoint(
        status="healthy",
        timestamp=uptime_info.current_time,
        uptime_seconds=uptime_info.uptime_seconds,
    )
