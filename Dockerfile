FROM python:3.10-slim AS build

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN python3 -m venv .venv; \
    . .venv/bin/activate; \
    python3 -m pip install poetry -q; \
    python3 -m poetry export -o requirements.txt; \
    deactivate; \
    rm -rf .venv;


FROM build as runtime

RUN useradd -ms /bin/bash caspian_app
USER caspian_app

RUN python3 -m pip install -r requirements.txt --user --no-deps
EXPOSE ${CASPIAN_PORT}

ENTRYPOINT [ "python3", "-m", "api" ]


FROM runtime AS caspian_api_dev
RUN which python3


FROM runtime AS caspian_api
COPY ./api ./api

