# Docker best practices applied
## Non-root user
Running application as non-root user
limits priviliges inside container,
prohibits system file modification,
provides kubernetes compatibility
and limits priviliges in case of container escape.

All of stated above improves security
and compatibility of image.
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
# ...
USER appuser
CMD ["fastapi", "run", "app.py"]
```

## Spesific base image version
Specifying version of base image
gives reproducibility for building
image from source.
```dockerfile
FROM python:3.12-slim
```

## Only copy necessary files
```dockerfile
COPY ./app.py .
```

## Proper layer ordering
Ordering dependency installation
before copying all files allows
docker to not reinstall dependencies
if there was changes only in code,
therefore saving time on building image.
```dockerfile
RUN useradd --create-home --shell /bin/bash appuser
EXPOSE 8000

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app.py .
```

## `.dockerignore` file
`.dockerignore` prevents docker from copying
certain files from working directory, thus
hiding vulnerable data (such as secrets, API keys and etc.)
and lowering image size through avoiding unnecessary files
such as documentation, IDE configurations,version control and other.
```
# Version control
.git
.gitignore

# Secrets
.env
*.pem
secrets/

# Documentation
*.md
docs/

# Tests
tests/

# IDE configurations
.vscode/
.idea/

# Python
__pycache__
*.py[oc]
venv
.venv
```


# Image Information & Decisions
## Base image
I have chosen `python:3.13-slim` image
since app not size-critical enough to
use alpine variant, but i do not need
compilation tools and slim variant is much
smaller than basic python image.

## Final image size
190 MB

## Layer structure and optimizations explanation
First, dockerfile creates user for
non-root running and exposes port 8000.
Since there is nothing to change, then
this stage is performed only once and
cached for all future builds.

Second, dockerfile copies `requirements.txt` and
runs `pip install` on them to prepare dependencies.
If this file have not changed since last build
(which is rarely the case in comparison with code changes),
then this stage is skipped too, therefore saving tens of
seconds of installing all dependencies.

Third, dockerfile copies application files
(exactly one in this case) and runs it as
non-root user. This stage is most likely
not to be skipped, since code is changed
oftenly, therefore most probable to run
stage should be in the end of dockerfile.


# Build & Run Process
## Complete terminal output from build process
```
[+] Building 20.9s (11/11) FINISHED                                                                            docker:default
 => [internal] load build definition from Dockerfile                                                                     0.0s
 => => transferring dockerfile: 361B                                                                                     0.0s
 => [internal] load metadata for docker.io/library/python:3.13-slim                                                      1.3s
 => [internal] load .dockerignore                                                                                        0.0s
 => => transferring context: 231B                                                                                        0.0s
 => [1/6] FROM docker.io/library/python:3.13-slim@sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b  1.8s
 => => resolve docker.io/library/python:3.13-slim@sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b  0.0s
 => => sha256:8843ea38a07e15ac1b99c72108fbb492f737032986cc0b65ed351f84e5521879 1.29MB / 1.29MB                           0.7s
 => => sha256:0bee50492702eb5d822fbcbac8f545a25f5fe173ec8030f57691aefcc283bbc9 11.79MB / 11.79MB                         1.4s
 => => sha256:36b6de65fd8d6bd36071ea9efa7d078ebdc11ecc23d2426ec9c3e9f092ae824d 249B / 249B                               1.0s
 => => sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b18 10.37kB / 10.37kB                         0.0s
 => => sha256:fbc43b66207d7e2966b5f06e86f2bc46aa4b10f34bf97784f3a10da80b1d6f0b 1.75kB / 1.75kB                           0.0s
 => => sha256:dd4049879a507d6f4bb579d2d94b591135b95daab37abb3df9c1d40b7d71ced0 5.53kB / 5.53kB                           0.0s
 => => extracting sha256:8843ea38a07e15ac1b99c72108fbb492f737032986cc0b65ed351f84e5521879                                0.1s
 => => extracting sha256:0bee50492702eb5d822fbcbac8f545a25f5fe173ec8030f57691aefcc283bbc9                                0.3s
 => => extracting sha256:36b6de65fd8d6bd36071ea9efa7d078ebdc11ecc23d2426ec9c3e9f092ae824d                                0.0s
 => [internal] load build context                                                                                        0.0s
 => => transferring context: 63B                                                                                         0.0s
 => [2/6] RUN useradd --create-home --shell /bin/bash appuser                                                            0.2s
 => [3/6] WORKDIR /app                                                                                                   0.0s
 => [4/6] COPY requirements.txt .                                                                                        0.0s
 => [5/6] RUN pip install --no-cache-dir -r requirements.txt                                                            17.2s
 => [6/6] COPY ./app.py .                                                                                                0.0s
 => exporting to image                                                                                                   0.3s
 => => exporting layers                                                                                                  0.3s
 => => writing image sha256:e63cd5678a4792a6b3105ab4c8268d899b31376a76bb790b365c6bf126c2907b                             0.0s
 => => naming to docker.io/library/infoservice:python-dev                                                                0.0s
```


## Terminal output of container running
```
   FastAPI   Starting production server 🚀

             Searching for package file structure from directories with
             __init__.py files                                   
2026-01-27 15:40:23,902 - app - INFO - Application starting...
             Importing from /app

    module   🐍 app.py

      code   Importing the FastAPI app object from the module with the following
             code:                                               

             from app import app

       app   Using import string: app:app

    server   Server started at http://0.0.0.0:8000
    server   Documentation at http://0.0.0.0:8000/docs

             Logs:

      INFO   Started server process [1]
2026-01-27 15:40:23,919 - uvicorn.error - INFO - Started server process [1]
      INFO   Waiting for application startup.
2026-01-27 15:40:23,920 - uvicorn.error - INFO - Waiting for application startup.
      INFO   Application startup complete.
2026-01-27 15:40:23,920 - uvicorn.error - INFO - Application startup complete.
      INFO   Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
2026-01-27 15:40:23,921 - uvicorn.error - INFO - Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
2026-01-27 15:40:26,267 - app - INFO - Collecting general information...
      INFO   172.17.0.1:36228 - "GET / HTTP/1.1" 200
2026-01-27 15:40:36,034 - app - INFO - Collecting general information...
      INFO   172.17.0.1:46442 - "GET / HTTP/1.1" 200
2026-01-27 15:41:57,231 - app - INFO - Collecting service health information...
      INFO   172.17.0.1:54722 - "GET /health HTTP/1.1" 200
^C
      INFO   Shutting down
2026-01-27 15:42:45,067 - uvicorn.error - INFO - Shutting down
      INFO   Waiting for application shutdown.
2026-01-27 15:42:45,169 - uvicorn.error - INFO - Waiting for application shutdown.
      INFO   Application shutdown complete.
2026-01-27 15:42:45,170 - uvicorn.error - INFO - Application shutdown complete.
      INFO   Finished server process [1]
2026-01-27 15:42:45,171 - uvicorn.error - INFO - Finished server process [1]
```

## Terminal output from testing endpoints
- root
```
{"service":{"name":"DevOps Info Service","version":"0.0.1","description":"DevOps course info service","framework":"fastapi"},"system":{"hostname":"7349c843900b","platform":"Linux","platform_version":"#1-NixOS SMP PREEMPT_DYNAMIC Thu Jan  8 09:15:06 UTC 2026","architecture":"x86_64","python_version":"3.13.11"},"runtime":{"uptime_seconds":2,"uptime_human":"0 hours, 0 minutes","current_time":"2026-01-27T15:40:26.267899+00:00","timezone":"UTC"},"request":{"client_ip":"172.17.0.1","user_agent":"curl/8.17.0","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Service information"},{"path":"/health","method":"GET","description":"Health check"}]}
```
- health
```
{"status":"healthy","timestamp":"2026-01-27T15:41:57.231209+00:00","uptime_seconds":93}
```

## Registry
[Link to Docker registry](https://hub.docker.com/repository/docker/ub3rch/infoservice/general)


# Technical analysis
My dockerfile works the way it does,
because I wrote it the way I wrote it.

Build time will increase, since docker
will perform stages, which can be skipped
(due to caching)
if they were performed in different oreder.

I implemented following security considerations:
- Non-root user running
- Hiding secrets with dockerfile

`.dockerignore` improves my build through
lowering image size and improving security.


# Challenges & Solutions
I have not encountered any major issues
with lab implementation, since I already
have some experience with docker
from other courses.
However that experience was a little bit old,
therefore I improved through repetion
and recall of known material, with addition of
new material such non-root user running.
