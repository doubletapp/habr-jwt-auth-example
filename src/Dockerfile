FROM python:3.10.7-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.1.13

WORKDIR /src/

RUN apt-get update && apt-get -y install libgdal-dev \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY src/ .

CMD ["uvicorn", "app.internal.main:app", "--host", "0.0.0.0", "--port", "8000"]
