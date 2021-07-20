# Prelims

- the whole project is managed by `poetry`
- using  `git` and `black` for VCS and formatting

# Basic Usage

- To start running the API server, use:
```bash
poetry run uvicorn api.main:app --reload
```

This should start the server in **develop** mode

Navigating to: http://127.0.0.1:8000/docs opens up the swagger api for fast api

- running tests:
make sure that the server is running

```bash
poetry run pytest
```

- running CRON job
```bash
poetry run python -m api.cron
```
