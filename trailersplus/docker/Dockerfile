# base image
FROM python:3.9-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        postgresql-client \
        binutils \
        libproj-dev \
        gdal-bin \
        libgdal-dev \
        libmemcached-dev \
        libsasl2-dev \
        libssl-dev \
        libpq-dev \
        curl \
        git \
        && rm -rf /var/lib/apt/lists/*

# set working directory
WORKDIR /app

# copy requirements file
COPY ./requirements.txt /app/

# install requirements
RUN pip install -r requirements.txt

# copy project files
COPY . /app
