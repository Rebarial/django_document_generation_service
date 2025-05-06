FROM python:latest

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && \
    apt-get install -y locales && \
    echo "ru_RU.UTF-8 UTF-8" > /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

RUN apt-get update && apt-get install -y curl libreoffice && rm -rf /var/lib/apt/lists/*

COPY ./src src

COPY .env .env

ENV PYTHONPATH /src/src

WORKDIR /src/src
