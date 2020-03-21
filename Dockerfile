FROM python:3.7-alpine
# MAINTAINER Snigdha, Sachin
LABEL maintainer="Snigdha, Sachin"

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Setup directory structure
RUN mkdir /website
WORKDIR /website
COPY ./website/ /website

RUN adduser -D user
USER user