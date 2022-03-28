FROM python:3.8-slim-buster
ENV PYTHONBUFFERED=1
WORKDIR /usr/src/pageloot_test_task
COPY . .
RUN pip3 install -r requirements.txt