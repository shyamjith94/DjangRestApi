FROM python:3.6-alpine
MAINTAINER Data Analyst Shyam

ENV PYTHONUNBUFFERED 1

# INSTALL DEPENDENCIES
COPY ./requirements.txt /requirements.txt

# POSTGRESS INSTALL
# jpeg-dev musl-dev zlib zlib-ded image library postgresql

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt

# DEELETE THAT TEMP REQUIREMNTS
RUN apk del .tmp-build-deps

# SET UP DIRECTORY STRUCTURE
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# FOR STATIC FILES
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
# CHANGE DIRECTORY PERMISSION AND OWNERSHIP BEFORE SWITCH USER
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web

USER user
