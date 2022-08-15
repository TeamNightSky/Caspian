FROM python:3
WORKDIR /backend

COPY poetry.lock /backend/
COPY pyproject.toml /backend/
RUN pip install poetry
RUN poetry install
COPY ./backend/ .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]