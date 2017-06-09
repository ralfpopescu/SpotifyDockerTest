FROM python:3.5

RUN mkdir -p /opt/app
WORKDIR /opt/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY spotifything.py spotifything.py
