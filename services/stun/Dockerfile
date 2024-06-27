FROM python:3.11-slim

ENV DockerHome=/home/services

# create the working directory
RUN mkdir -p ${DockerHome}

ARG ARTIFACTORY_BH_USER
ARG ARTIFACTORY_BH_PASS

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy the working directory
COPY requirements.txt ${DockerHome}

# set the working directory
WORKDIR ${DockerHome}

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy the working directory
COPY . ${DockerHome}

CMD ["python3", "-u", "./src/main.py"]