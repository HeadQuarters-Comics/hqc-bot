# set base image (host OS)
FROM python:3.10.8-slim

ENV SERVICE=/home/app

ENV PYTHONUNBUFFERED=1

RUN mkdir -p $SERVICE

# set the working directory in the container
WORKDIR $SERVICE

# Download latest listing of available packages:
RUN apt-get -y update

# Upgrade already installed packages:
RUN apt-get -y upgrade

COPY requirements.txt .

RUN pip install --upgrade pip

RUN apt-get -y install gcc
RUN apt-get -y install libpq-dev 

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local app directory to the working directory
COPY . .

# command to run on container start
CMD [ "python", "./main.py" ]