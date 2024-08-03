FROM python:3.13.0b4-alpine
# MAINTAINER Snigdha, Sachin
LABEL maintainer="Snigdha, Sachin"

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
# installing postgresql client
# --no-cache reason: minimize the no. of extra files
# and packages that are included in the docker conatiner
RUN apk add --update --no-cache postgresql-client
# making sure docker has absolutly minimal footprint (no extra dependencies)
# sets up a alias for our dependecies and remove them later(temporary dependencies)
RUN apk add --update --no-cache --virtual .tmp-build-dps \
        gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt
# removing temporary dependencies
RUN apk del .tmp-build-dps 

# Setup directory structure
RUN mkdir /website
WORKDIR /website
COPY ./website/ /website

RUN adduser -D user
USER user