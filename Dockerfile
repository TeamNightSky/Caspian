FROM python:3.10 as system_packages

RUN apt update -yq && apt install -yq ffmpeg

FROM system_packages AS python_dependencies

WORKDIR /app
COPY pyproject.toml ./

# Export the dependencies
ENV PATH=$PATH:/root/.local/bin
RUN python3 -m venv .venv; \
    . .venv/bin/activate; \
    python3 -m pip install poetry -q; \
    python3 -m poetry lock; \
    python3 -m poetry export -o requirements.txt; \
    deactivate; \
    rm -rf .venv pyproject.toml poetry.lock; \
    python3 -m pip install -q -r requirements.txt --no-deps --user;

COPY ./api /app/api

FROM python_dependencies as caspian_api

ENTRYPOINT [ "python3", "-m", "api" ]

FROM python_dependencies as caspian_worker

ENTRYPOINT [ "celery", "-A", "api.worker", "worker", "-l", "info" ]


