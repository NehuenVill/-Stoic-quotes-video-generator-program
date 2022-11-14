FROM python:alpine

COPY . /app

WORKDIR /app

CMD python video_generation.py

