FROM python:3.10-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl unzip gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN apt-get remove -y curl unzip gcc python3-dev

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 2087

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python manage.py collectstatic --noinput