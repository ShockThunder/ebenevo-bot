# syntax=docker/dockerfile:1

# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt /app/

# Install required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/
# Копируем файл .env в контейнер
COPY .env /app/.env  

CMD ["python", "./main.py"]