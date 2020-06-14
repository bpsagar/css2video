FROM python:latest

RUN apt-get update -y && \
    apt-get install -y cutycapt ffmpeg xvfb

ADD . /app

WORKDIR /app

RUN pip install .

