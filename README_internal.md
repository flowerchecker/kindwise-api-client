## Setup

```bash
conda env create
conda activate kindowse-sdk
poetry install
pre-commit install
pre-commit install --hook-type commit-msg
```

## Tests

Specify server used for testing via environmental variable `ENVIRONMENT`.

- LOCAL: usually used for development on one system which is run locally
- STAGING: default
- PRODUCTION
