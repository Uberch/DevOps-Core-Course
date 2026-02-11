# Overview
## Testing Framework
I have chosen pytest as testing framework,
since it is simple and powerful and
adding this dependency will not cause
critical slowing of CI.

## Test Coverage
### Test Structure Explanation
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

### Running Tests Locally
From `app_python` directory:
```bash
source venv/bin/activate
pytest
```

### Terminal Output
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

## CI workflow trigger configuration
### Trigger Strategy and Reasoning
Workflow triggers on pushes and
PR's to master branch 
(assuming changes in application
or workflow)

## Versioning strategy
Semantic versioning
because it represents my
progress with course.

# Workflow evidence

# Best Practices
- Job Dependencies: Dont do work,
which will fail, because previous
work failed
- Pull Request Checks: Prevents
bad code in master branch, productions
- Fail Fast: Catch errors as early as possible
- Caching:
- Snyk not done, since snyk blocks Russian users

# Key decisions
## Versioning Strategy
I have decided to use
Semantic versioning of type
"python-<lab_number>.1.0"

## Docker tags
My workflow creates two tags:
- python-<version>
- latest

## Wokflow triggers
The workflow is triggerred on
push, this allows fast feedback
on each delivered change.

Also workflow triggers on pull
requests to prevent merging of
bad code to master branch.

## Test coverage
What is covered:
System- and Client- dependend outputs
(to prevent occasional hard-coding)

What is not covered:
Getters, setters and
hardcoded(intentionally)
outputs
