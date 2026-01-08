## Setup

```bash
conda env create
conda activate kindowse-sdk
pipx install poetry==2.2.1
poetry install --extras router
pre-commit install
pre-commit install --hook-type commit-msg
```

## Developmnet

Do not directly modify files under `kindwise/sync` directory. The ground truth code is located in `kindwise/async_api` directory. Use the following command to generate sync code from async code:

```bash
poetry run python generate/generate_sync_code.py
# or
make generate-sync
```
## Tests

Specify server used for testing via environmental variable `ENVIRONMENT`.

- LOCAL: usually used for development on one system which is run locally
- STAGING: default
- PRODUCTION
