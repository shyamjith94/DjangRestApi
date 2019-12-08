FROM python:3.6-alpine
MAINTAINER Data Analyst Shyam

ENV PYTHONUNBUFFERED 1

# INSTALL DEPENDENCIES
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# SET UP DIRECTORY STRUCTURE
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
