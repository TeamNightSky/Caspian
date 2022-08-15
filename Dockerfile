FROM python:3.10

WORKDIR /caspian
COPY . .

ARG DIR

RUN if [ ! -z $DIR ]; then echo /caspian_volume >> dir; else echo /caspian >> dir; fi

RUN adduser --disabled-password app
RUN chown -R app /caspian

USER app

RUN pip install -U poetry
RUN python -m poetry config virtualenvs.in-project true --local

EXPOSE ${CASPIAN_PORT}

USER root

ENTRYPOINT sh docker-entrypoint.sh $(cat dir)
