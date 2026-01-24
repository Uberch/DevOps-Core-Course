"""
DevOps Info Service
Main application module
"""

# Imports
import os
import socket
import platform
import logging
import uvicorn
from datetime import datetime, timezone
from fastapi import FastAPI, Request


# Configuration
DEBUG = logging.DEBUG if os.getenv('DEBUG', 'False').lower() == 'true' else logging.INFO

logging.basicConfig(
    level=DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Application starting...")


# Application start time
START_TIME = datetime.now(timezone.utc)
start_time = datetime.now()

app = FastAPI(
    title="DevOps Info Service",
    description="DevOps course info service",
    summary="",
    version="0.0.1",
)


# Various information collecting functions
def get_system_info():
    """Collect system information."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": platform.python_version()
    }

def get_uptime():
    delta = datetime.now() - start_time
    seconds = int(delta.total_seconds())
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return {
        "uptime_seconds": seconds,
        "uptime_human": f"{hours} hours, {minutes} minutes",
        "current_time": datetime.now(timezone.utc).isoformat(),
        "timezone": str(timezone.utc),
    }

def get_endpoints():
    return [
        {
            "path": "/",
            "method": "GET",
            "description": "Service information",
        },
        {
            "path": "/health",
            "method": "GET",
            "description": "Health check",
        },
    ]


# FastAPI
@app.get("/")
def index(request: Request):
    """Main endpoint - service and system information."""
    logger.info("Collecting general information...")
    logger.debug(f'Request: {request.method} {request.url.path}')
    return {
        "service": {
            "name": app.title,
            "version": app.version,
            "description": app.description,
            "framework": "fastapi",
        },
        "system": get_system_info(),
        "runtime": get_uptime(),
        "request": {
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent"),
            "method": request.method,
            "path": request.url.path,
        },
        "endpoints": get_endpoints(),
    }

@app.get("/health")
def health(request: Request):
    """Health endpoint - information about services status"""
    logger.info("Collecting service health information...")
    logger.debug(f'Request: {request.method} {request.url.path}')
    return {
        "status": "healthy",
        "timestamp": get_uptime()["current_time"],
        "uptime_seconds": get_uptime()["uptime_seconds"],
    }
