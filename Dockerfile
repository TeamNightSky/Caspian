FROM python:3.10-slim AS build

WORKDIR "/app"
COPY pyproject.toml poetry.lock ./
RUN python3 -m venv .venv; \
    . .venv/bin/activate; \
    .venv/bin/pip3 install poetry; \
    .venv/bin/python3 -m poetry install
EXPOSE ${CASPIAN_PORT}

FROM build AS dev
RUN ls
ENTRYPOINT [ "./.venv/bin/python", "-m", "api" ]


FROM build AS prod
COPY ./api ./api

ENTRYPOINT [ "./.venv/bin/python", "-m", "api" ]

