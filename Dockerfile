FROM ubuntu:16.04

MAINTAINER delgemoon "delgemoon@gmail.com"

RUN mkdir /app

WORKDIR /app
ADD * /app/
RUN apt-get -y update
RUN apt-get -y install python3-pip python3-dev 
RUN apt-get -y install librtmp-dev libffi-dev 	 
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]

