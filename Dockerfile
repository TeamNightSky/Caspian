FROM python:3.10 as build

RUN apt update -yq
RUN apt install -yq apt-utils
RUN apt install -yq ffmpeg


FROM build AS dependencies

WORKDIR /app
COPY pyproject.toml ./

# Export the dependencies
RUN python3 -m venv .venv; \
    . .venv/bin/activate; \
    python3 -m pip install poetry -q; \
    python3 -m poetry lock; \
    python3 -m poetry export -o requirements.txt; \
    deactivate; \
    rm -rf .venv pyproject.toml poetry.lock;

ENV PATH=$PATH:/root/.local/bin
RUN python3 -m pip install -q -r requirements.txt --no-deps --user

FROM dependencies as caspian_api
EXPOSE ${CASPIAN_PORT}
COPY ./api /app/api
ENTRYPOINT [ "python3", "-m", "api" ]


