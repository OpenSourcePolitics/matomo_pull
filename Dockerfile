FROM ubuntu:latest
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /workdir
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 
RUN apt-get install -y python3-pip 
RUN apt-get install -y poppler-utils 
RUN apt-get install -y libpq-dev 
RUN apt-get install -y libsm6 libxext6 libxrender-dev
RUN apt-get install -y postgresql

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
ENV PORT 8080
ENV TIMEOUT 1200
CMD gunicorn -w 4 --bind=0.0.0.0:${PORT} app:app --timeout=${TIMEOUT}