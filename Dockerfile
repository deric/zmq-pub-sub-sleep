FROM python:3.6-slim-stretch

ENV LANG C.UTF-8
RUN apt-get update && apt-get upgrade -y\
 && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install pyzmq==17.0.0

ENV APP_DIR /app

RUN mkdir -p /app && chown -R www-data:www-data /app
ADD pub.py /app
ADD sub.py /app

WORKDIR /app
EXPOSE 6500
