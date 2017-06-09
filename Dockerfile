FROM python:3.5

RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
COPY . /
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["spotifything.py"]
