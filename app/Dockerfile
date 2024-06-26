FROM python:3.11-slim

RUN mkdir -p /app/data

RUN mkdir -p /app/input

RUN mkdir -p /app/logs

RUN mkdir -p /app/src

WORKDIR /app/src

ENV TZ="Asia/Jakarta"

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

WORKDIR /app

CMD ["fastapi", "run", "src/app.py", "--port", "80"]

