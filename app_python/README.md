# Overview
Simple service for collecting system and service information

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

# Running the Application
```bash
fastapi run app.py
```
Or with custom config:
```bash
PORT=8000 fastapi run app.py
```

# API Endpoints
- `GET /` - Service and system information
- `GET /health` - Health check

# Configuration
| Variable name | Type | Default value | Example
|---|---|---|---|
| PORT | Integer | 5000 | 8000 |
| DEBUG | Boolean | false | true |
