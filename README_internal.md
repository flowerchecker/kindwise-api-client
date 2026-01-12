## Setup

```bash
conda env create
conda activate kindowse-sdk
pipx install poetry==2.2.1
poetry install --extras router
pre-commit install
pre-commit install --hook-type commit-msg
make generate-sync
```

## Developmnet

Do not directly modify files under `kindwise` directory. The ground truth code is located in `kindwise/async_api` directory. Use the following command to generate sync code from async code:

```bash
python generate/generate_sync_code.py
# or
make generate-sync
```
## Tests

Specify server used for testing via environmental variable `ENVIRONMENT`.

- LOCAL: usually used for development on one system which is run locally
- STAGING: default
- PRODUCTION


## Deployment

```bash
# Bump version
#
# if changes are not backward compatible, use "major"
make version-major
# if changes are backward compatible, use "minor" and some new features are added
make version-minor
# if only bug fixes, use "patch"
make version-patch

# Publish to PyPI
make publish
```

### Test project

Test deployment by using the test project in `test_project` directory. More information can be found in [test project README](test_project/README.md).


> **Note:** If you are developing the SDK locally and want to test changes, you can install the SDK in editable mode from the parent directory instead of from PyPI:
> ```bash
> pip install -e ..
> ```
> And remove `kindwise-api-client` from `requirements.txt` before running the install command above.