# Dockerfile
FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 安裝基本系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "luvsmallfamily.wsgi:application"]