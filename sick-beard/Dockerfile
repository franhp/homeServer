FROM ubuntu:14.04
MAINTAINER franhp@te.chie.la

RUN apt-get -y update
RUN apt-get -y install git\
                    python\
                    python-pip


RUN mkdir /app
RUN echo 2 && git clone https://github.com/franhp/Sick-Beard.git app
WORKDIR /app

EXPOSE 8081

CMD python SickBeard.py
