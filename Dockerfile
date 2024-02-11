FROM python:3.11-slim
ARG NESTER_LISTEN_PORT
ARG FLASK_LISTEN_PORT
WORKDIR .

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.env config.env

COPY /src /src
EXPOSE $NESTER_LISTEN_PORT
EXPOSE $FLASK_LISTEN_PORT
CMD ["python", "./src/app.py"]