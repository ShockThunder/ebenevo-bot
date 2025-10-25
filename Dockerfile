# syntax=docker/dockerfile:1

# Use Python 3.10 as base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first for better caching
COPY requirements.txt /app/

# Install required packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Create data directory if it doesn't exist
RUN mkdir -p /app/data

# Command to run the Python script
CMD ["python", "main.py"]