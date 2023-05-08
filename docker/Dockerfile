FROM python:3.8

RUN mkdir /app
WORKDIR app

ADD requirements.txt /app/

# SetUp environment veriables
# Disable creating .pyc files
ENV PYTHONDONTWRITBYTECODE 1
# Force the stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
# Use default answers for all questions
ENV DEBIAN_FRONTEND=noninteractive

# Install all dependencies
RUN pip3 install --upgrade pip &&\
    pip3 install -r requirements.txt

ADD trailersplus /app/
RUN chmod -R 0600 /app/trailersplus/certs/psql/client-key.pem
EXPOSE 8000
