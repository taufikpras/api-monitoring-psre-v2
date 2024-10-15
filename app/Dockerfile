FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/src

RUN mkdir -p /app/data

RUN mkdir -p /app/input

RUN mkdir -p /app/logs

ENV TZ="Asia/Jakarta"

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["fastapi", "run", "src/app.py", "--port", "80"]

