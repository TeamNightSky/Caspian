#!/bin/sh

chown -R app $0
cd $(cat dir)
touch .env

su -c "python -m poetry install && python -m poetry run python backend/manage.py runserver 0.0.0.0:$CASPIAN_PORT" app
