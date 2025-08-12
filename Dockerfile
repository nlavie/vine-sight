FROM python:3.11
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
ENV APP_HOME /app
ENV PYTHONUNBUFFERED True
ENV PORT 9090
ENV PYTHONPATH="${APP_HOME}:${APP_HOME}:${PYTHONPATH}"
WORKDIR $APP_HOME

COPY . /app
COPY ./Pipfile.lock ./
COPY ./Pipfile ./

RUN pip install pipenv
RUN pipenv install

RUN pipenv run gunicorn --version

CMD ["pipenv", "run", "gunicorn", "--bind", ":$PORT", "--workers", "1", "--threads", "8", "--timeout", "0", "python", "main:app"]