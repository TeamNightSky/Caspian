FROM python:3.10-slim as build

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Export the dependencies
RUN python3 -m venv .venv; \
    . .venv/bin/activate; \
    python3 -m pip install poetry -q; \
    python3 -m poetry export -o requirements.txt; \
    deactivate; \
    rm -rf .venv;

FROM jrottenberg/ffmpeg:5.1-ubuntu as ffmpeg

FROM build as runtime
COPY --from=ffmpeg /usr/local /usr/local
RUN python3 -m pip install -r requirements.txt --user --no-deps

EXPOSE ${CASPIAN_PORT}
ENTRYPOINT [ "python3", "-m", "api" ]


FROM runtime AS caspian_api_dev

FROM runtime AS caspian_api
COPY ./api ./api

