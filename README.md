# DjangRestApi
Django Rest Api Project Files
Using two app 
  - one core 
      - store core files of app
      - data base test using manage.py
      - custom user model store in core app
  - two user
      - other auth and other functions


# mysql Docker

FROM python:3.6-alpine
MAINTAINER SHYAMJITH

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps \
        mariadb-dev \
        gcc \
        musl-dev \
    && pip install mysqlclient==1.4.5 \
    && apk del .build-deps
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user


# mysql Requirements

django>=3.0,<=3.0
djangorestframework>=3.10.3,<=3.10.3
django-mysql>1.3
