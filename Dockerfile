FROM python:3.11-slim
WORKDIR .

RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY config.env config.env

COPY /src /src

CMD ["python", "./src/app.py"]