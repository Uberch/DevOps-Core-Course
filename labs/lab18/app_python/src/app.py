"""
DevOps Info Service
Main application module
"""

# Imports
import os
from pydoc import tempfile_pager
import socket
import platform
import logging
import json
import time
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


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


class VisitsEndpoint(BaseModel):
    count: int


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


def increase_visit_count():
    count_file = "/data/visits"
    temp_file = "/data/visits.temp"
    while os.path.isfile(temp_file):
        pass
    with open(temp_file, "w") as t_file:
        count = read_visit_count()
        _ = t_file.write(str(count+1))
        os.replace(temp_file, count_file)


def read_visit_count():
    count_file = "/data/visits"
    if os.path.isfile(count_file):
        with open(count_file, "r") as file:
            return int(file.read())
    else: return 0


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
registry = CollectorRegistry()


# Prometheus metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=registry,
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    registry=registry,
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently being processed',
    registry=registry,
)

endpoint_calls = Counter(
    'devops_info_endpoint_calls',
    'Endpoint calls',
    ['endpoint'],
    registry=registry,
)

system_info_duration = Histogram(
    'devops_info_system_collection_seconds',
    'System info collection time',
    registry=registry,
)


@app.middleware("http")
async def middleware(request: Request, call_next):
    logger.info(f'Request: {request.method} {request.url.path}')
    start_time = time.time()

    response = await call_next(request)

    path = request.url.path

    duration = time.time() - start_time
    http_requests_total.labels(
        method=request.method,
        endpoint=path,
        status=str(response.status_code),
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=path,
    ).observe(duration)

    logger.info(f'Response code: {response.status_code}.')
    return response


# FastAPI
@app.get("/")
@http_requests_in_progress.track_inprogress()
def index(request: Request):
    increase_visit_count()
    """Main endpoint - service and system information."""
    logger.info("Collecting general information...")

    start_time = time.time()
    sys_info = get_system_info()
    duration = time.time() - start_time
    system_info_duration.observe(duration)

    return MainEndpoint(
        system=sys_info,
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
@http_requests_in_progress.track_inprogress()
def health():
    """Health endpoint - information about services status"""
    logger.info("Collecting service health information...")
    uptime_info = get_uptime()
    return HealthEndpoint(
        status="healthy",
        timestamp=uptime_info.current_time,
        uptime_seconds=uptime_info.uptime_seconds,
    )


@app.get("/metrics")
def metrics():
    return PlainTextResponse(
        generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/visits")
def visits():
    return VisitsEndpoint(count=read_visit_count())
