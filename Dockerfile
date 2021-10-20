FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJ_DIR /fastapi-practice

COPY . $PROJ_DIR
WORKDIR $PROJ_DIR
RUN pip install -r requirements.txt