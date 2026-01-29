# Overview
Simple service for collecting system and service information

# Prerequisites
No additional dependencies if installed as executable

If builded from source code, then you need:
- go
- gcc

# Installation
Building from source code
```bash
git clone https://github.com/Uberch/DevOps-Core-Course.git
cd DevOps-Core-Course/go_app
go build
```

# Running the Application
```bash
./infoService
```

Or with custom config:
```bash
PORT=8000 ./infoService
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
docker run -i -rm -p <port_number>:8000 <image_name>:<tag> .
```

## Pulling from Docker Hub
```bash
docker pull ub3rch/infoservice:go-<version>
docker tag ub3rch/infoservice:go-<version> <image_name>:<tag> 
```
