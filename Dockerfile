FROM ubuntu:14.04
MAINTAINER franhp@te.chie.la

RUN apt-get -y update
RUN apt-get -y install git\
                        python \
                        python-pip \
                        python-setuptools \
                        python-dev \
                        python-mysqldb \
                        cython \
                        libavcodec-dev \
                        libavformat-dev \
                        libswscale-dev \
                        libxml2-dev \
                        libxslt-dev \
                        zlib1g-dev

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app
RUN cd /app && pip install -r requirements.txt

ADD . /app

EXPOSE 8000

CMD gunicorn -w 4 home.wsgi -b 0.0.0.0:8000
