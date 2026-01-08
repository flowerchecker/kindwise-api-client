## Setup

```bash
conda env create
conda activate kindowse-sdk
pipx install poetry==2.2.1
poetry install --extras router
pre-commit install
pre-commit install --hook-type commit-msg
```

## Tests

Specify server used for testing via environmental variable `ENVIRONMENT`.

- LOCAL: usually used for development on one system which is run locally
- STAGING: default
- PRODUCTION
