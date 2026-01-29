# Unit testing
## Testing Framework Choose
I have chosen pytest as testing framework,
since it is simple and powerful and
adding this dependency will not cause
critical slowing of CI.

## Test Structure Explanation
- test_endpoint_main():
Ensures main endpoint
is present and checks right,
platform-dependent output.
- test_endpoint_health():
Ensures healt endpoint is present.
- test_request_info(mocker):
Test the main endpoint
response from simulated
different ip's and user agents.

## Terminal Output
```
====================== test session starts ======================
platform linux -- Python 3.13.11, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/uber/code/DevOps/app_python
configfile: pyproject.toml
plugins: anyio-4.12.1, mock-3.15.1
collected 3 items

tests/test_sample.py ...                                  [100%]
================= 3 passed, 0 warning in 0.29s ==================
```

# GitHub Actions CI Workflow
## Trigger Strategy and Reasoning
Since I create separate branch
for each lab, I have decided to
trigger CI with pull request to
`master` branch. This way I
initially create pull request
and each time I push to branch,
pull request is updated and
CI is triggered.

## Choise of specific actions
- action/checkout@v4 - needed to clone repo
- action/setup-python@v5 - needed to setup python
- snyk/action/python-3.10@master - scans security
- docker/login-action@v3 - login to docker registry
- docker/build-push-action@v5 - builds and pushes docker image

## Docker tagging strategy
I have decided to use semantic versioning of type
"python-<lab_number>.x.y"

## ![Succesful Workflow](https://github.com/Uberch/DevOps-Core-Course/actions/runs/21480050436)

## Screenshot
[Succesful Workflow](./screenshots/workflow.png)

# CI Best Practices & Security
## Caching implementation and speed improvement metrics

## CI Best Practices Applied

## Snyk integration

## Improved Workflow Performance
