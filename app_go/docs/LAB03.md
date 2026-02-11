# GitHub Actions CI Workflow
- Job Dependencies
- Pull Request Checks
- Fail Fast

# Path filter configuration
## Configuration
```YAML
on:
  pull_request:
    branches: [ master ]
  push:
    paths:
      - 'app_go/**'
      - '.github/workflows/go-ci.yml'
      - '!app_go/docs'
      - '!app_go/README.md'
      - '!**.gitignore'
```

## Benefits analysis
Path filters allow to save
CI time (and, therefore money)
by disabling rerunning 
workflows related to unchanged code.

## Selective Triggering

# Test Coverage
## Integration
## Analysis
| Dimension | Python | Go |
|---|---|---|
| Current percentage | 99 | 0 |
| Threshold | 70 | 70 |
What is covered:
- Python: System- and Client- dependend outputs
(to prevent occasional hard-coding)

- Go: Nothing

What is not covered:
- Python: getters, setters and
hardcoded outputs

- Go: Everything
