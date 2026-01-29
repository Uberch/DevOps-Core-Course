# Overview
Simple service for collecting system and service information

# CI/CD Status
[![Python CI](https://github.com/Uberch/DevOps-Core-Course/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Uberch/DevOps-Core-Course/actions/workflows/python-ci.yml)

# Prerequisites
- python 3.13

# Installation
```bash
git clone https://github.com/Uberch/DevOps-Core-Course.git
cd DevOps-Core-Course
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Testing the Application
```bash
cd app_python
pytest
```

# Running the Application
```bash
fastapi run infoservice/app.py
```
Or with custom config:
```bash
PORT=8000 fastapi run infoservice/app.py
```

# API Endpoints
- `GET /` - Service and system information
- `GET /health` - Health check

# Configuration
| Variable name | Type | Default value | Example
|---|---|---|---|
| PORT | Integer | 8000 | 8080 |
| DEBUG | Boolean | false | true |

# Docker
## Buidling image
```bash
docker build -t <image_name>:<tag> .
```

## Running container
```bash
docker run -rm -p <port_number>:8000 <image_name>:<tag> .
```

## Pulling from Docker Hub
```bash
docker pull ub3rch/infoservice:python-<version>
docker tag ub3rch/infoservice:python-<version> <image_name>:<tag> 
```
