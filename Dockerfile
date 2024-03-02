FROM python:3.10-slim

WORKDIR /app

ARG SERVER_PORT_ARG

RUN apt-get update \
    && apt-get install -y curl gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $SERVER_PORT

RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations
RUN python manage.py migrate
