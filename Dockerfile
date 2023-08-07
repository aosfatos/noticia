FROM docker.io/python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /project

RUN apt-get update && \
    apt-get install vim -y

COPY requirements.txt /project/
RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r /project/requirements.txt


COPY . /project
